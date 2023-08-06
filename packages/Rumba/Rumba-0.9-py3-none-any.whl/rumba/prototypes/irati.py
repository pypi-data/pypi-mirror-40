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

import copy
import json
import os
import time

import rumba.ssh_support as ssh
import rumba.model as mod
import rumba.multiprocess as m_processing
import rumba.prototypes.irati_templates as irati_templates
import rumba.log as log

logger = log.get_logger(__name__)


class Experiment(mod.Experiment):
    """
    Represents an IRATI experiment.
    """

    @staticmethod
    def make_executor(node, packages, testbed):
        def executor(commands):
            ssh.aptitude_install(testbed, node, packages)
            node.execute_commands(commands, time_out=None, use_proxy=True)
        return executor

    def prototype_name(self):
        return 'irati'

    @staticmethod
    def real_sudo(s):
        return 'sudo ' + s

    @staticmethod
    def fake_sudo(s):
        return s

    def __init__(self, testbed,
                 nodes=None,
                 git_repo='https://github.com/IRATI/stack',
                 git_branch='arcfire',
                 installpath=None,
                 varpath=None,
                 app_mappings=None,
                 enrollment_strategy='minimal'):
        """
        Initializes the experiment class.

        :param testbed: The testbed to run the experiment on.
        :param nodes: The list of nodes.
        :param git_repo: The git repository to use for installation.
        :param git_branch: The branch of the git repository to use.
        :param installpath: The installation path of IRATI.
        :param varpath: The /var path of IRATI.
        :param app_mappings: a list of application -> dif mapping containing
                             all application which will register to
                             any given dif.
        :type app_mappings: `List[(str, str)]`
        :param enrollment_strategy: Can be 'full-mesh', 'minimal' or 'manual'.
        """
        mod.Experiment.__init__(self,
                                testbed,
                                nodes,
                                git_repo,
                                git_branch,
                                prototype_logs=['/tmp/ipcmstart.log'],
                                enrollment_strategy=enrollment_strategy)
        if installpath is None:
            installpath = '/usr'
        if varpath is None:
            varpath = ''
        irati_templates.env_dict['installpath'] = installpath
        irati_templates.env_dict['varpath'] = varpath
        self.manager = False
        self.conf_files = None
        self.shim2vlan = {}

        if app_mappings is None:
            app_mappings = []
        self.app_mappings = app_mappings

        if self.testbed.username == 'root':
            self.sudo = self.fake_sudo
        else:
            self.sudo = self.real_sudo

        self._conf_dir = os.path.join(mod.tmp_dir, 'IRATI_conf')
        try:
            os.mkdir(self._conf_dir)
        except OSError:
            # Already there, nothing to do
            pass

    def conf_dir(self, path):
        return os.path.join(self._conf_dir, path)

    def install(self):

        packages = ["g++", "gcc", "libtool", "linux-headers-$(uname -r)",
                    "autoconf", "automake", "protobuf-compiler",
                    "libprotobuf-dev", "git", "pkg-config", "libssl-dev"]

        cmds = [self.sudo("rm -rf ~/stack"),
                "cd ~; git clone -b " + self.git_branch + " " + self.git_repo,
                "cd ~/stack && "
                + self.sudo("./configure && ") + self.sudo("make install")]
        names = []
        executors = []
        args = []
        for node in self.nodes:

            executor = self.make_executor(node, packages, self.testbed)

            names.append(node.name)
            executors.append(executor)
            args.append(cmds)
        m_processing.call_in_parallel(names, args, executors)

    def bootstrap_network(self):
        for node in self.nodes:
            self.process_node(node)
        self.enroll_nodes()

    def _install_prototype(self):
        logger.info("installing IRATI on all the nodes")
        self.install()
        logger.info("installation complete")

    def _bootstrap_prototype(self):
        logger.info("setting up")
        self.conf_files = self.write_conf()
        logger.info("configuration files generated for all nodes")
        self.bootstrap_network()
        logger.info("IPCPs created and enrolled on all nodes")

    def process_node(self, node):
        name = node.name

        vlans = []
        for ipcp in node.ipcps:
            if isinstance(ipcp, mod.ShimEthIPCP):
                vlans.append([ipcp.ifname, self.shim2vlan[ipcp.dif.name]])

        if vlans:
            ssh.setup_vlans(self.testbed, node, vlans)

        gen_files_conf = self.conf_files[node] + ['da.map']
        dir_path = os.path.dirname(os.path.abspath(__file__))
        gen_files_bin = 'enroll.py'
        gen_files_conf_full = [self.conf_dir(x) for x in gen_files_conf]
        gen_files_bin_full = [os.path.join(dir_path, 'enroll.py')]

        ipcm_components = ['scripting', 'console']
        if self.manager:
            ipcm_components.append('mad')
        ipcm_components = ', '.join(ipcm_components)

        gen_files = gen_files_conf_full + gen_files_bin_full

        format_args = {'name': name,
                       'ssh': node.ssh_config.port,
                       'username': self.testbed.username,
                       'genfiles': gen_files,
                       'genfilesconf': ' '.join(gen_files_conf),
                       'genfilesbin': gen_files_bin,
                       'verb': 'DBG',
                       'ipcmcomps': ipcm_components}

        logger.info('Copying configuration files to node %s', node.name)
        ssh.copy_files_to_testbed(self.testbed,
                                  node.ssh_config,
                                  gen_files,
                                  '')

        cmds = [self.sudo('hostname %(name)s' % format_args),
                self.sudo('modprobe rina-irati-core'),
                self.sudo('chmod a+rw /dev/irati'),
                # The || true should be removed soon, but it's needed
                # until we update the bitbucket repo.
                self.sudo('chmod a+rw /dev/irati-ctrl || true'),
                self.sudo('mv %(genfilesconf)s /etc' % format_args),
                self.sudo('mv %(genfilesbin)s /usr/bin') % format_args,
                self.sudo('chmod a+x /usr/bin/enroll.py') % format_args]

        cmds += [self.sudo('modprobe rina-default-plugin'),
                 self.sudo('modprobe shim-eth-vlan'),
                 self.sudo('modprobe normal-ipcp'),
                 self.sudo('ipcm -a \"%(ipcmcomps)s\" '
                           '-c /etc/%(name)s.ipcm.conf -l %(verb)s '
                           '> /tmp/ipcmstart.log 2>&1 &'
                           % format_args)]

        logger.info('Sending setup commands to node %s.', node.name)
        ssh.execute_commands(self.testbed, node.ssh_config, cmds)

    def enroll_nodes(self):
        logger.info("Starting enrollment phase.")
        time.sleep(5)
        for enrollment_list in self.enrollments:
            for e in enrollment_list:
                logger.info(
                    'Enrolling %s to DIF %s against neighbor %s,'
                    ' through lower DIF %s.',
                    e['enrollee'].name,
                    e['dif'].name,
                    e['enroller'].name,
                    e['lower_dif'].name)

                time.sleep(1)  # Important!

                e_args = {'ldif': self.dif_name(e['lower_dif']),
                          'dif': e['dif'].name,
                          'nname': e['enrollee'].node.name,
                          'iname': e['enrollee'].name,
                          'o_iname': e['enroller'].name}

                cmd = self.sudo('enroll.py --lower-dif %(ldif)s --dif %(dif)s '
                                '--ipcm-conf /etc/%(nname)s.ipcm.conf '
                                '--enrollee-name %(iname)s.IPCP '
                                '--enroller-name %(o_iname)s.IPCP'
                                % e_args)
                ssh.execute_command(self.testbed,
                                    e['enrollee'].node.ssh_config,
                                    cmd)

    def dif_name(self, dif):
        try:
            return str(self.shim2vlan[dif.name])
        except KeyError:
            return dif.name

    def write_conf(self):
        # Constants and initializations
        ipcmconfs = dict()
        difconfs = dict()
        ipcp2shim_map = {}
        node2id_map = {}
        mgmt_dif_name = 'NMS'
        conf_files = {}  # dict of per-nod conf files

        # Translating Shim Eth difs to vlan tags.
        next_vlan = 10
        for dif in self.dif_ordering:
            if isinstance(dif, mod.ShimEthDIF):
                try:
                    vlan = int(dif.name)
                    self.shim2vlan[dif.name] = vlan
                except ValueError:
                    vlan = next_vlan
                    next_vlan += 10
                    self.shim2vlan[dif.name] = vlan

        # If some app directives were specified, use those to build da.map.
        # Otherwise, assume the standard applications are to be mapped in
        # the DIF with the highest rank.
        app_mappings = self.app_mappings
        if len(app_mappings) == 0:
            if len(self.dif_ordering) > 0:
                for adm in \
                        irati_templates.da_map_base["applicationToDIFMappings"]:
                    adm["difName"] = "%s" % (self.dif_ordering[-1].name,)
        else:  # not yet supported
            irati_templates.da_map_base["applicationToDIFMappings"] = []
            for app, dif in app_mappings:
                irati_templates.da_map_base["applicationToDIFMappings"]\
                    .append({"encodedAppName": app,
                             "difName": dif
                             })

        if self.manager:
            # Add MAD/Manager configuration
            irati_templates.get_ipcmconf_base()["addons"] = {
                "mad": {
                    "managerAppName": "",
                    "NMSDIFs": [{"DIF": "%s" % mgmt_dif_name}],
                    "managerConnections": [{
                        "managerAppName": "manager-1--",
                        "DIF": "%s" % mgmt_dif_name
                    }]
                }
            }

        node_number = 1
        for node in self.nodes:  # type: mod.Node
            node2id_map[node.name] = node_number
            node_number += 1
            ipcmconfs[node.name] = copy.deepcopy(irati_templates.get_ipcmconf_base())
            if self.manager:
                ipcmconfs[node.name]["addons"]["mad"]["managerAppName"] \
                    = "%s.mad-1--" % (node.name,)

        for dif in self.dif_ordering:  # type: mod.DIF
            if isinstance(dif, mod.ShimEthDIF):
                ipcp2shim_map.update({ipcp.name: dif for ipcp in dif.ipcps})
            elif isinstance(dif, mod.NormalDIF):
                difconfs[dif.name] = dict()
                # Generate base conf
                dif_conf = copy.deepcopy(irati_templates.normal_dif_base)
                # push qos_cubes
                if len(dif.qos_cubes) != 0:
                    dif_conf["qosCubes"] = []
                    for cube in dif.qos_cubes:
                        dif_conf["qosCubes"].append(
                            irati_templates.generate_qos_cube(**cube)
                        )
                    if dif.add_default_qos_cubes:
                        # Add basic cubes
                        unreliable = copy.deepcopy(irati_templates.qos_cube_u_base)
                        unreliable["id"] = len(dif_conf["qosCubes"]) + 1
                        dif_conf["qosCubes"].append(unreliable)
                        reliable = copy.deepcopy(irati_templates.qos_cube_r_base)
                        reliable["id"] = len(dif_conf["qosCubes"]) + 1
                        dif_conf["qosCubes"].append(reliable)

                for node in dif.members:
                    difconfs[dif.name][node.name] = copy.deepcopy(
                        dif_conf
                    )

        for node in self.nodes:  # type: mod.Node
            ipcmconf = ipcmconfs[node.name]

            for ipcp in node.ipcps:  # type: mod.ShimEthIPCP
                if isinstance(ipcp, mod.ShimEthIPCP):
                    shim = ipcp2shim_map[ipcp.name]  # type: mod.ShimEthDIF
                    shim_name = self.dif_name(shim)
                    ipcmconf["ipcProcessesToCreate"].append({
                        "apName": "eth.%s.IPCP" % ipcp.name,
                        "apInstance": "1",
                        "difName": shim_name
                    })

                    template_file_name = self.conf_dir(
                        'shimeth.%s.%s.dif'
                        % (node.name, shim_name))
                    ipcmconf["difConfigurations"].append({
                        "name": shim_name,
                        "template": os.path.basename(template_file_name)
                    })

                    fout = open(template_file_name, 'w')
                    fout.write(json.dumps(
                        {"difType": "shim-eth-vlan",
                         "configParameters": {
                             "interface-name": ipcp.ifname
                         }
                         },
                        indent=4, sort_keys=True))
                    fout.close()
                    conf_files.setdefault(node, []).append(
                        'shimeth.%s.%s.dif'
                        % (node.name, shim_name))

        # Run over dif_ordering array, to make sure each IPCM config has
        # the correct ordering for the ipcProcessesToCreate list of operations.
        # If we iterated over the difs map, the order would be randomic, and so
        # some IPCP registrations in lower DIFs may fail.
        #  This would happen because at the moment of registration,
        #  it may be that the IPCP of the lower DIF has not been created yet.
        shims = ipcp2shim_map.values()
        for dif in self.dif_ordering:  # type: mod.NormalDIF

            if dif in shims:
                # Shims are managed separately, in the previous loop
                continue

            for node in dif.members:  # type: mod.Node
                node_name = node.name
                ipcmconf = ipcmconfs[node_name]

                normal_ipcp = {"apName": "%s.%s.IPCP" % (dif.name, node_name),
                               "apInstance": "1",
                               "difName": "%s" % (dif.name,),
                               "difsToRegisterAt": []}

                for lower_dif in node.dif_registrations[dif]:  # type: mod.DIF
                    normal_ipcp["difsToRegisterAt"].append(
                        self.dif_name(lower_dif))

                ipcmconf["ipcProcessesToCreate"].append(normal_ipcp)

                ipcmconf["difConfigurations"].append({
                    "name": "%s" % (dif.name,),
                    "template": "normal.%s.%s.dif" % (node_name, dif.name,)
                })

                # Fill in the map of IPCP addresses.
                # This could be moved at difconfs
                for other_node in dif.members:  # type: mod.Node
                    difconfs[dif.name][other_node.name] \
                        ["knownIPCProcessAddresses"].append({
                         "apName": "%s.%s.IPCP" % (dif.name, node_name),
                         "apInstance": "1",
                         "address": 16 + node2id_map[node_name]})
                policy_dict = node.get_policy(dif).get_policies()
                for component in policy_dict:
                    for policy_name in policy_dict[component]:
                        params = policy_dict[component][policy_name].items()
                        irati_templates.translate_policy(
                            difconfs[dif.name][node_name],
                            component,
                            policy_name,
                            params
                        )

        # Dump the DIF Allocator map
        with open(self.conf_dir('da.map'), 'w') as da_map_file:
            json.dump(irati_templates.da_map_base,
                      da_map_file,
                      indent=4,
                      sort_keys=True)

        for node in self.nodes:
            # Dump the IPCM configuration files
            with open(self.conf_dir('%s.ipcm.conf'
                                    % (node.name,)), 'w') as node_file:
                json.dump(ipcmconfs[node.name],
                          node_file,
                          indent=4,
                          sort_keys=True)
            conf_files.setdefault(node, []).append(
                '%s.ipcm.conf' % (node.name,))

        for dif in self.dif_ordering:  # type: mod.DIF
            dif_conf = difconfs.get(dif.name, None)
            if dif_conf:
                # Dump the normal DIF configuration files
                for node in dif.members:
                    with open(self.conf_dir('normal.%s.%s.dif'
                                            % (node.name, dif.name)), 'w') \
                            as dif_conf_file:
                        json.dump(dif_conf[node.name],
                                  dif_conf_file,
                                  indent=4,
                                  sort_keys=True)
                    conf_files.setdefault(node, []).append(
                        'normal.%s.%s.dif' % (node.name, dif.name))
        return conf_files

    def _terminate_prototype(self):
        return
