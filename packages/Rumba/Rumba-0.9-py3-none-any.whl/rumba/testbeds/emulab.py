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

import os
import time
import re
from ast import literal_eval
import warnings

import rumba.ssh_support as ssh
import rumba.model as mod
import rumba.log as log

from rumba.executors.ssh import SSHExecutor


logger = log.get_logger(__name__)


warnings.filterwarnings("ignore")

class Testbed(mod.Testbed):
    """
    Represents an emulab testbed.
    """
    def __init__(self, exp_name, username, proj_name,
                 password="", url="wall2.ilabt.iminds.be",
                 image=None):
        """
        Initializes the testbed class.

        :param exp_name: The experiment name.
        :param username: User of the experiment.
        :param password: Password of the user.
        :param proj_name: Project name of the experiment.
        :param url: URL of the testbed.
        :param image: Specific image to use.
        """
        mod.Testbed.__init__(self, exp_name, username, password, proj_name)
        self.url = url
        self.image = image
        self.ip = dict()
        self.ops_ssh_config = mod.SSHConfig(self._ops_server())

        self.executor = SSHExecutor

    def _ops_server(self):
        """
        Return server name of the ops-server (is testbed specific).

        :return: Server name of the ops-server.
        """
        return 'ops.' + self.url

    def _full_name(self, node_name):
        """
        Return server name of a node.

        :param node_name: Name of the node.
        :return: Server name of the node.
        """
        return node_name + '.' + self.exp_name + '.' + \
            self.proj_name + '.' + self.url

    def _get_experiment_list(self, project_name=None):
        """
        Get list of made emulab experiments accessible with your credentials.

        :param project_name: Optional filter on project.
        :return: List of created experiments.
        """
        cmd = '/usr/testbed/bin/sslxmlrpc_client.py -m experiment getlist'
        out = ssh.execute_command(self, self.ops_ssh_config, cmd)

        try:
            if project_name is not None:
                return literal_eval(out)[project_name][project_name]
            else:
                return literal_eval(out)
        except:
            return {project_name: {project_name: []}}

    def _swap_exp_in(self):
        """
        Swaps experiment in.

        :return: Is the experiment newly swapped in?
        """
        cmd = '/usr/testbed/bin/sslxmlrpc_client.py swapexp proj=' + \
              self.proj_name + \
              ' exp=' + \
              self.exp_name + \
              ' direction=in'

        try:
            ssh.execute_command(self, self.ops_ssh_config, cmd)
        except ssh.SSHException as e:
            line = re.findall(r'not swapped out', str(e))
            if line:
                logger.info("Experiment is already swapped in.")
                return False
            else:
                raise e

        return True

    def _create_experiment(self, experiment):
        """
        Creates an emulab experiment

        :param experiment: The experiment.
        """
        proj_name = self.proj_name
        exp_name = self.exp_name

        exp_list = self._get_experiment_list()

        try:
            if exp_name in exp_list[proj_name][proj_name]:
                logger.info("Experiment already exists.")
                return
        except:
            logger.info("First experiment to be created for that project.")

        ns = self._generate_ns_script(experiment)
        dest_file_name = '/users/' + self.username + \
                         '/temp_ns_file.%s.ns' % os.getpid()
        ssh.write_text_to_file(self, self.ops_ssh_config, ns, dest_file_name)

        cmd = '/usr/testbed/bin/sslxmlrpc_client.py startexp ' + \
              'batch=false wait=true proj="' + proj_name + \
              '" exp="' + exp_name + '" noswapin=true ' + \
              'nsfilepath="' + dest_file_name + '"'

        try:
            ssh.execute_command(self, self.ops_ssh_config, cmd, time_out=None)
            logger.info("New experiment succesfully created.")
        except:
            logger.info("Experiment already exists.")
        finally:
            ssh.execute_command(self, self.ops_ssh_config,
                                'rm ' + dest_file_name)

    def _generate_ns_script(self, experiment):
        """
        Generate ns script based on network graph.
        Enables to customize default node image.

        :param experiment: The experiment.
        :return: ns2 script for Emulab experiment.
        """

        ns2_script = "# ns script generated by Rumba\n"
        ns2_script += "set ns [new Simulator]\n"
        ns2_script += "source tb_compat.tcl\n"

        for node in experiment.nodes:
            ns2_script += "set " + node.name + " [$ns node]\n"
            if self.image is not None:
                ns2_script += "tb-set-node-os $" + node.name + " " + \
                    self.image + "\n"

        for dif in experiment.dif_ordering:
            if isinstance(dif, mod.ShimEthDIF):
                if len(dif.ipcps) != 2:
                    continue
                ns2_script += "set " + dif.name + \
                              " [$ns duplex-link $" + \
                              dif.members[0].name + " $" + \
                              dif.members[1].name + " 1000Mb 0ms DropTail]\n"

        ns2_script += "$ns run\n"

        return ns2_script

    def _wait_until_nodes_up(self):
        """
        Checks if nodes are up.
        """
        logger.info("Waiting until all nodes are up")

        cmd = '/usr/testbed/bin/script_wrapper.py expinfo -e' + \
              self.proj_name + \
              ',' + \
              self.exp_name + \
              ' -a | grep State | cut -f2,2 -d " "'

        res = ssh.execute_command(self, self.ops_ssh_config, cmd)
        active = False
        if res == "active":
            active = True
        while not active:
            res = ssh.execute_command(self, self.ops_ssh_config, cmd)
            if res == "active":
                active = True
            logger.info("Still waiting")
            time.sleep(5)

    def _complete_experiment_graph(self, experiment):
        """
        Gets the interface (ethx) to link mapping.

        :param experiment: The experiment.
        """

        for node in experiment.nodes:
            node.ssh_config.hostname = self._full_name(node.name)
            node.ssh_config.set_username(self.username)
            node.ssh_config.set_password(self.password)

        cmd = 'cat /var/emulab/boot/topomap'
        topomap = node.execute_command(cmd)
        # Almost as ugly as yo momma
        index = topomap.rfind("# lans")
        topo_array = topomap[:index].split('\n')[1:-1]
        # Array contains things like 'r2b1,link7:10.1.6.3 link6:10.1.5.3'
        for item in topo_array:
            item_array = re.split(',? ?', item)
            node_name = item_array[0]
            for item2 in item_array[1:]:
                item2 = item2.split(':')
                link_name = item2[0]
                link_ip = item2[1]
                for node in experiment.nodes:
                    if node.name != node_name:
                        continue
                    for ipcp in node.ipcps:
                        if ipcp.dif.name == link_name:
                            self.ip[ipcp] = link_ip

        for node in experiment.nodes:
            cmd = 'cat /var/emulab/boot/ifmap'
            output = node.execute_command(cmd)
            output = re.split('\n', output)
            for item in output:
                item = item.split()
                for ipcp in node.ipcps:
                    if isinstance(ipcp, mod.ShimEthIPCP):
                        if self.ip[ipcp] == item[1]:
                            ipcp.ifname = item[0]

    def _swap_in(self, experiment):
        """
        Swaps experiment in

        :param experiment: The experiment.
        """
        self._create_experiment(experiment)
        wait = self._swap_exp_in()
        if wait:
            self._wait_until_nodes_up()
        self._complete_experiment_graph(experiment)

        if "wall" in self.url:
            for node in experiment.nodes:
                ssh_support.set_http_proxy(self, node_n,
                                           "https://proxy.atlantis."
                                           "ugent.be:8080")

    def _swap_out(self, experiment):
        """
        Swaps experiment out

        :param experiment: The experiment.
        """
        cmd = '/usr/testbed/bin/sslxmlrpc_client.py swapexp proj=' + \
              self.proj_name + \
              ' exp=' + \
              self.exp_name + \
              ' direction=out'

        ssh.execute_command(self, self.ops_ssh_config, cmd)
