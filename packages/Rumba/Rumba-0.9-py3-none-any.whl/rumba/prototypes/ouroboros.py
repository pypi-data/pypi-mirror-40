#
# A library to manage ARCFIRE experiments
#
#    Copyright (C) 2017-2018 Nextworks S.r.l.
#    Copyright (C) 2017-2018 imec
#
#    Sander Vrijders   <sander.vrijders@ugent.be>
#    Dimitri Staessens <dimitri.staessens@ugent.be>
#    Vincenzo Maffione <v.maffione@nextworks.it>
#    Marco Capitani    <m.capitani@nextworks.it>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., http://www.fsf.org/about/contact/.
#

import time
import subprocess
import re

import rumba.ssh_support as ssh
import rumba.model as mod
import rumba.multiprocess as m_processing
import rumba.log as log
import rumba.testbeds.local as local
import rumba.testbeds.dockertb as docker
import rumba.storyboard as sb

logger = log.get_logger(__name__)


class OurServer(sb.Server):

    def __init__(self, server):
        super(OurServer, self).__init__(
            server.ap,
            server.arrival_rate,
            server.actual_parameter + server.min_duration,
            server.options,
            server.max_clients,
            server.clients,
            server.nodes,
            server.min_duration,
            server.id,
            server.as_root,
            server.difs
        )

    def _make_run_cmd(self, node):
        o_cmd = super(OurServer, self)._make_run_cmd(node)

        # Run and store PID
        n_cmd = 'pid=$(%s) && ' % (o_cmd,)

        # Build register command
        r_cmd = 'irm r n %s ' % (self.id,)
        if len(self.difs) == 0:
            r_cmd += ' '.join('ipcp %s' % (ipcp.name,) for ipcp in node.ipcps)
        else:
            for dif in self.difs:
                for ipcp in node.ipcps:
                    if ipcp.dif is dif:
                        r_cmd += 'ipcp %s' % (ipcp.name,)
        r_cmd += ' && '

        # Add register command
        n_cmd += r_cmd

        # Add bind command
        n_cmd += 'irm b process $pid name %s && ' % (self.id,)

        n_cmd += 'echo $pid'  # We need to return the pid for the sb

        return n_cmd


class Experiment(mod.Experiment):
    """
    Represents an Ouroboros experiment.
    """
    def __init__(self,
                 testbed,
                 nodes=None,
                 git_repo='git://ouroboros.ilabt.imec.be/ouroboros',
                 git_branch='master',
                 enrollment_strategy='minimal',
                 flows_strategy='full-mesh'):
        """
        Initializes the experiment class.

        :param testbed: The testbed to run the experiment on.
        :param nodes: The list of nodes.
        :param git_repo: The git repository to use for installation.
        :param git_branch: The branch of the git repository to use.
        :param enrollment_strategy: Can be 'full-mesh', 'minimal' or 'manual'.
        :param strategy: For flows, 'full-mesh', 'minimal' or 'manual'.
        """
        mod.Experiment.__init__(
            self,
            testbed,
            nodes,
            git_repo,
            git_branch,
            enrollment_strategy=enrollment_strategy,
            flows_strategy=flows_strategy,
            server_decorator=OurServer
        )
        self.r_ipcps = dict()

        self.set_startup_command("irmd")

    @staticmethod
    def make_executor(node, packages, testbed):
        def executor(commands):
            ssh.aptitude_install(testbed, node, packages)
            node.execute_commands(commands, time_out=None, use_proxy=True)
        return executor

    def prototype_name(self):
        return 'ouroboros'

    def exec_local_cmd(self, cmd):
        try:
            logger.info(cmd)
            subprocess.check_call(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            logger.error("Return code was " + str(e.returncode))
            raise

    def exec_local_cmds(self, cmds):
        for cmd in cmds:
            self.exec_local_cmd(cmd)

    def setup_ouroboros(self):
        if isinstance(self.testbed, docker.Testbed):
            return

        if isinstance(self.testbed, local.Testbed):
            subprocess.check_call('sudo -v'.split())
            self.irmd = subprocess.Popen(["sudo", "irmd"])
            logger.info("Started IRMd, sleeping 2 seconds...")
            time.sleep(2)
        else:
            for node in self.nodes:
                node.execute_command("sudo nohup irmd > /dev/null &",
                                     time_out=None)

    def install_ouroboros(self):
        if isinstance(self.testbed, local.Testbed):
            return

        packages = ["cmake", "protobuf-c-compiler", "git", "libfuse-dev",
                    "libgcrypt20-dev", "libssl-dev"]

        fs_loc = '/tmp/prototype'

        cmds = ["sudo apt-get install libprotobuf-c-dev --yes || true",
                "sudo rm -r " + fs_loc + " || true",
                "git clone -b " + self.git_branch + " " + self.git_repo + \
                " " + fs_loc,
                "cd " + fs_loc + " && mkdir build && cd build && " +
                "cmake .. && " +
                "sudo make install -j$(nproc)"]

        names = []
        executors = []
        args = []

        for node in self.nodes:
            executor = self.make_executor(node, packages, self.testbed)
            names.append(node.name)
            executors.append(executor)
            args.append(cmds)
        m_processing.call_in_parallel(names, args, executors)

    def create_ipcps(self):
        for node in self.nodes:
            cmds = list()
            for ipcp in node.ipcps:
                cmds2 = list()
                if ipcp.dif_bootstrapper:
                    cmd = "irm i b n " + ipcp.name
                else:
                    cmd = "irm i c n " + ipcp.name

                if isinstance(ipcp.dif, mod.ShimEthDIF):
                    if isinstance(self.testbed, local.Testbed):
                        cmd += " type local layer " + ipcp.dif.name
                    else:
                        cmd += " type eth-dix dev " + ipcp.ifname
                        cmd += " layer " + ipcp.dif.name
                elif isinstance(ipcp.dif, mod.NormalDIF):
                    cmd += " type normal"
                    if ipcp.dif_bootstrapper:
                        pols = ipcp.dif.policy.get_policies()
                        for comp in pols:
                            for pol in pols[comp]:
                                cmd += " " + comp + " " + pol
                        cmd += " layer " + ipcp.dif.name + " autobind"

                        cmd2 = "irm r n " + ipcp.name
                        for dif_b in node.dif_registrations[ipcp.dif]:
                            for ipcp_b in node.ipcps:
                                if ipcp_b in dif_b.ipcps:
                                    cmd2 += " ipcp " + ipcp_b.name
                        cmds2.append(cmd2)
                        cmd2 = "irm r n " + ipcp.dif.name
                        for dif_b in node.dif_registrations[ipcp.dif]:
                            for ipcp_b in node.ipcps:
                                if ipcp_b in dif_b.ipcps:
                                    cmd2 += " ipcp " + ipcp_b.name
                        cmds2.append(cmd2)
                elif isinstance(ipcp.dif, mod.ShimUDPDIF):
                    # FIXME: Will fail, since we don't keep IPs yet
                    cmd += " type udp"
                    cmd += " layer " + ipcp.dif.name
                else:
                    logger.error("Unsupported IPCP type")
                    continue

                cmds.append(cmd)
                # Postpone registrations
                self.r_ipcps[ipcp] = cmds2

            node.execute_commands(cmds, time_out=None)

    def enroll_dif(self, el):
        for e in el:
            ipcp = e['enrollee']
            cmds = list()

            # Execute postponed registration
            if e['enroller'] in self.r_ipcps:
                e['enroller'].node.execute_commands(self.r_ipcps[e['enroller']],
                                                    time_out=None)
                self.r_ipcps.pop(e['enroller'], None)

            cmd = "irm r n " + ipcp.name
            for dif_b in e['enrollee'].node.dif_registrations[ipcp.dif]:
                for ipcp_b in e['enrollee'].node.ipcps:
                    if ipcp_b in dif_b.ipcps:
                        cmd += " ipcp " + ipcp_b.name
            cmds.append(cmd)
            cmd = "irm i e n " + ipcp.name + " layer " + e['dif'].name + \
                  " autobind"
            cmds.append(cmd)
            cmd = "irm r n " + ipcp.dif.name
            for dif_b in e['enrollee'].node.dif_registrations[ipcp.dif]:
                for ipcp_b in e['enrollee'].node.ipcps:
                    if ipcp_b in dif_b.ipcps:
                        cmd += " ipcp " + ipcp_b.name
            cmds.append(cmd)

            e['enrollee'].node.execute_commands(cmds, time_out=None)

    def setup_flows(self, el):
        for e in el:
            ipcp = e['src']
            cmd = "irm i conn n " + ipcp.name + " dst " + e['dst'].name
            retry = 0
            max_retries = 3
            while retry < max_retries:
                time.sleep(retry * 5)
                try:
                    ipcp.node.execute_command(cmd, time_out=None)
                    break
                except Exception as e:
                    retry += 1
                    logger.error('Failed to connect IPCP, retrying: ' +
                                 str(retry) + '/' + str(max_retries) +
                                 ' retries')
            if retry == max_retries:
                raise Exception('Failed to connect IPCP')

    def _install_prototype(self):
        logger.info("Installing Ouroboros...")
        self.install_ouroboros()
        logger.info("Installed on all nodes...")

    def _bootstrap_prototype(self):
        for dif in self.dif_ordering:
            if isinstance(dif, mod.NormalDIF):
                if len(dif.qos_cubes) != 0:
                    logger.warn('QoS cubes not (yet) supported by '
                                'the Ouroboros plugin. Will ignore.')
        logger.info("Starting IRMd on all nodes...")
        self.setup_ouroboros()
        logger.info("Creating IPCPs")
        self.create_ipcps()
        logger.info("Enrolling IPCPs...")

        for enrolls, flows in zip(self.enrollments,
                                self.flows):
            self.enroll_dif(enrolls)
            self.setup_flows(flows)

        logger.info("All done, have fun!")

    def _terminate_prototype(self, force=False):
        cmds = list()

        if force is True:
            kill = 'killall -9 '
            cmds.append(kill + 'irmd')
            cmds.append(kill + 'ipcpd-normal')
            cmds.append(kill + 'ipcpd-shim-eth-llc')
            cmds.append(kill + 'ipcpd-local')
            cmds.append('kill -9 $(ps axjf | grep \'sudo irmd\' '
                        '| grep -v grep | cut -f4 -d " "')
        else:
            cmds.append('killall -15 irmd')

        logger.info("Killing Ouroboros...")
        if isinstance(self.testbed, local.Testbed):
            cmds = list(map(lambda c: "sudo %s" % (c,), cmds))
            for cmd in cmds:
                subprocess.check_call(cmd.split())
        else:
            for node in self.nodes:
                node.execute_commands(cmds, time_out=None, as_root=True)

    def destroy_dif(self, dif):
        for ipcp in dif.ipcps:
            ipcp.node.execute_command('irm i d n ' + ipcp.name)

    def parse_stats(self, lines, spaces=0):
        d = {}

        while len(lines):
            line = lines[0]

            if not re.match(" {%i}.*" % spaces, line):
                return d

            lines.pop(0)

            line = line.strip()

            if re.match(".*:.*", line):
                head, tail = line.split(":", 1)

                if len(tail) == 0:
                    d[head] = self.parse_stats(lines, spaces+1)
                else:
                    d[head] = tail.strip()

        return d


    def export_dif_bandwidth(self, filename, dif):
        f = open(filename, 'w')

        for node in dif.members:
            ipcp = node.get_ipcp_by_dif(dif)

            # Get IPCP address
            if not hasattr(ipcp, 'address'):
                path = '/tmp/ouroboros/'+ ipcp.name + '/dt*'
                dt_path = node.execute_command('ls -d %s' % path)
                dts = dt_path.split('.')
                ipcp.address = int(dts[-1])
                logger.info('IPCP %s has dt component '
                            'with address %d' % (ipcp.name, ipcp.address))

        for node in dif.members:
            ipcp = node.get_ipcp_by_dif(dif)

            dt_path = '/tmp/ouroboros/' + ipcp.name + '/dt.' + \
                str(ipcp.address) + '/'

            # Get flows to other endpoints
            fd = node.execute_command('ls --ignore=[01] %s' % dt_path)
            fds = fd.split('\n')
            for fd in fds:
                fd_path = dt_path + fd
                fd_file = node.execute_command('cat %s' % fd_path)

                d = self.parse_stats(fd_file.splitlines())
                remote = d["Endpoint address"]
                ipcp2_name = ''
                for ipcp2 in dif.ipcps:
                    if ipcp2.address == int(remote):
                        ipcp2_name = ipcp2.name

                nr = d["Qos cube   0"]["sent (bytes)"]

                f.write('%s;%s;%s\n' % (ipcp.name, ipcp2_name, nr))

        f.close()
        logger.info('Wrote stats to %s', filename)
