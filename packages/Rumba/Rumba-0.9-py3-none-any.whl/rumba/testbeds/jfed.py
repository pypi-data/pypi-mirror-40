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

import subprocess
import getpass
import xml.dom.minidom as xml
import os.path
import time
import tarfile
import sys

from rumba.executors.ssh import SSHExecutor

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

import rumba.model as mod
import rumba.log as log
from rumba import ssh_support

logger = log.get_logger(__name__)


class Testbed(mod.Testbed):
    """
    Represents a jFed testbed.
    """
    def __init__(self, exp_name, username, cert_file, exp_hours="2",
                 proj_name="rumba", authority="wall2.ilabt.iminds.be",
                 image=None, image_custom=False, image_owner=None,
                 use_physical_machines=None):
        """
        Initializes the testbed class.

        :param exp_name: The experiment name.
        :param username: User of the experiment.
        :param cert_file: Certificate file of the user.
        :param exp_hours: Duration of the experiment.
        :param proj_name: Project name of the experiment.
        :param authority: Actual testbed authority to use.
        :param image: Specific image to use.
        :param image_custom: Is the image a custom one?
        :param image_owner: Creator of the image.
        :param use_physical_machines: Try to allocate physical machines.

        .. note:: Supported authorities are wall1.ilabt.iminds.be,
                  wall2.ilabt.iminds.be, exogeni.net, exogeni.net:umassvmsite.
        """
        passwd = getpass.getpass(prompt="Password for certificate file: ")
        mod.Testbed.__init__(self,
                             exp_name,
                             username,
                             passwd,
                             proj_name)
        self.auth_name = authority
        self.cert_file = cert_file
        self.exp_hours = exp_hours
        self.if_id = dict()
        self.rspec = os.path.join(mod.tmp_dir, self.exp_name + ".rspec")
        self.manifest = os.path.join(mod.tmp_dir, self.exp_name + ".rrspec")
        self.jfed_jar = os.path.join(mod.cache_dir,
                                     'jfed_cli/experimenter-cli.jar')
        self.executor = SSHExecutor(self)

        if "exogeni" in authority:
            self.authority = "urn:publicid:IDN+" + authority + "+authority+am"
        elif "wall" in authority:
            self.authority = "urn:publicid:IDN+" + authority + "+authority+cm"
        elif "cloudlab" or "geniracks" in authority:
            self.authority = "urn:publicid:IDN+" + authority + "+authority+cm"
        else:
            logger.info("Authority may not be fully supported")
            self.authority = "urn:publicid:IDN+" + authority + "+authority+am"

        if use_physical_machines is None:
            if "wall" in authority or "cloudlab" in authority:
                self.use_physical_machines = True
            else:
                self.use_physical_machines = False

        if image is not None:
            if image_owner is None:
                if not image_custom:
                    image_owner = "emulab-ops"
                else:
                    if "wall" in authority:
                        image_owner = "wall2-ilabt-iminds-be"
                    else:
                        image_owner = "GeniSlices"
            self.image = "urn:publicid:IDN+" + authority + \
                         "+image+" + image_owner + ":" + image
        else:
            self.image = None

        if not os.path.exists(self.jfed_jar):
            logger.info("Couldn't find jFed CLI. Downloading.")
            tarball = "jfed_cli.tar.gz"
            url = "http://jfed.iminds.be/downloads/stable/jar/" + tarball
            urlretrieve(url, filename=tarball)
            tar = tarfile.open(tarball)
            tar.extractall()
            tar.close()
            os.rename(os.path.join(os.getcwd(), 'jfed_cli'),
                      os.path.join(mod.cache_dir, 'jfed_cli'))
            os.remove(tarball)
        self.flags['no_vlan_offload'] = True

    def _create_rspec(self, experiment):
        """
        Create an rspec which is an XML file with configuration for jFed.

        :param experiment: The experiment.
        :return: rspec of the experiment.
        """
        impl = xml.getDOMImplementation()
        doc = impl.createDocument(None, "rspec", None)

        top_el = doc.documentElement
        top_el.setAttribute("xmlns", "http://www.geni.net/resources/rspec/3")
        top_el.setAttribute("type", "request")
        top_el.setAttribute("xmlns:emulab", "http://www.protogeni.net/" +
                            "resources/rspec/ext/emulab/1")
        top_el.setAttribute("xmlns:jfedBonfire", "http://jfed.iminds.be/" +
                            "rspec/ext/jfed-bonfire/1")
        top_el.setAttribute("xmlns:delay", "http://www.protogeni.net/" +
                            "resources/rspec/ext/delay/1")
        top_el.setAttribute("xmlns:jfed-command", "http://jfed.iminds.be/" +
                            "rspec/ext/jfed-command/1")
        top_el.setAttribute("xmlns:client", "http://www.protogeni.net/" +
                            "resources/rspec/ext/client/1")
        top_el.setAttribute("xmlns:jfed-ssh-keys", "http://jfed.iminds.be/" +
                            "rspec/ext/jfed-ssh-keys/1")
        top_el.setAttribute("xmlns:jfed", "http://jfed.iminds.be/rspec/" +
                            "ext/jfed/1")
        top_el.setAttribute("xmlns:sharedvlan", "http://www.protogeni.net/" +
                            "resources/rspec/ext/shared-vlan/1")
        top_el.setAttribute("xmlns:xsi", "http://www.w3.org/2001/" +
                            "XMLSchema-instance")
        top_el.setAttribute("xsi:schemaLocation", "http://www.geni.net/" +
                            "resources/rspec/3 http://www.geni.net/" +
                            "resources/rspec/3/request.xsd")

        for node in experiment.nodes:
            el = doc.createElement("node")
            top_el.appendChild(el)
            el.setAttribute("client_id", node.name)

            if node.machine_type is None:
                if (self.use_physical_machines):
                    el.setAttribute("exclusive", "true")
                else:
                    el.setAttribute("exclusive", "false")
            elif node.machine_type == "virtual":
                el.setAttribute("exclusive", "false")
            else:
                el.setAttribute("exclusive", "true")

            el.setAttribute("component_manager_id", self.authority)

            el2 = doc.createElement("sliver_type")
            el.appendChild(el2)

            if (el.getAttribute("exclusive") == "true"):
                el2.setAttribute("name", "raw-pc")
            else:
                el2.setAttribute("name", "default-vm")

            if self.image is not None:
                image_el = doc.createElement("disk_image")
                image_el.setAttribute("name", self.image)
                el2.appendChild(image_el)

            node.ifs = 0
            for ipcp in node.ipcps:
                if isinstance(ipcp, mod.ShimEthIPCP):
                    el3 = doc.createElement("interface")
                    self.if_id[ipcp] = node.name + ":if" + str(node.ifs)
                    el3.setAttribute("client_id", self.if_id[ipcp])
                    node.ifs += 1
                    el.appendChild(el3)

        for dif in experiment.dif_ordering:
            if isinstance(dif, mod.ShimEthDIF):
                el = doc.createElement("link")
                top_el.appendChild(el)
                el.setAttribute("client_id", dif.name)

                el2 = doc.createElement("component_manager")
                el2.setAttribute("name", self.authority)
                el.appendChild(el2)

                for ipcp in dif.ipcps:
                    el3 = doc.createElement("interface_ref")
                    el3.setAttribute("client_id", self.if_id[ipcp])
                    el.appendChild(el3)

        file = open(self.rspec, "w")
        file.write(doc.toprettyxml())
        file.close()

    def _swap_out(self, experiment):
        """
        Swaps experiment out

        :param experiment: The experiment.
        """
        try:
            subprocess.check_call(["java", "-jar", self.jfed_jar, "delete",
                                   "-S", self.proj_name, "-s", self.exp_name,
                                   "-p", self.cert_file, "-P", self.password])
        except subprocess.CalledProcessError as e:
            logger.error("jFed returned with error " + str(e.returncode))
            raise

    def _swap_in(self, experiment):
        """
        Swaps experiment in

        :param experiment: The experiment.
        """
        self._create_rspec(experiment)

        auth_name_r = self.auth_name.replace(".", "-")

        for node in experiment.nodes:
            node.ssh_config.username = self.username
            node.ssh_config.password = self.password

        logger.info("Launching jFed...")

        try:
            subprocess.check_call(["java", "-jar", self.jfed_jar, "create",
                                   "-S", self.proj_name, "--rspec",
                                   self.rspec, "-s", self.exp_name, "-p",
                                   self.cert_file, "-k",
                                   "usercert,userkeys,shareduserallkeys",
                                   "--create-slice", "--manifest",
                                   self.manifest, "-P", self.password,
                                   "-e", self.exp_hours])
        except subprocess.CalledProcessError as e:
            logger.error("jFed returned with error " + str(e.returncode))
            raise

        if "exogeni" in self.auth_name:
            try:
                subprocess.check_call(["java", "-jar", self.jfed_jar,
                                       "manifest", "-S", self.proj_name,
                                       "-s", self.exp_name,
                                       "-p", self.cert_file,
                                       "--manifest", self.manifest,
                                       "-P", self.password])
            except subprocess.CalledProcessError as e:
                logger.error("jFed returned with error " + str(e.returncode))
                raise

        rspec = xml.parse(self.manifest)
        xml_nodes = rspec.getElementsByTagName("node")

        for xml_node in xml_nodes:
            n_name = xml_node.getAttribute("client_id")
            intfs = xml_node.getElementsByTagName("interface")

            node_n = None
            for node in experiment.nodes:
                if node.name == n_name:
                    node_n = node
                    break
            if node_n is None:
                logger.error("Didn't find node %s", n_name)

            if "wall" in self.auth_name:
                node_n.ssh_config.proxy_server = "bastion.test.iminds.be"

            s_node = xml_node.getElementsByTagName("services")[0]
            l_node = s_node.getElementsByTagName("login")[0]

            node_n.ssh_config.hostname = l_node.getAttribute("hostname")

            if "wall" in self.auth_name:
                ssh_support.set_http_proxy(self, node_n,
                                           "https://proxy.atlantis.ugent."
                                           "be:8080")

            ssh_support.execute_command(
                self,
                node_n.ssh_config,
                "sudo touch /var/lib/cloud/instance/locale-check.skip || true")

            for intf in intfs:
                aux_mac_address = intf.getAttribute("mac_address")

                if "wall" in self.auth_name:
                    mac = ":".join(
                        [aux_mac_address[i:i+2] for i in range(0, 12, 2)]
                    )
                else:
                    mac = aux_mac_address

                command = (
                    "echo '#!/usr/bin/env bash' > mac2ifname.sh; "
                    r"echo 'for i in $(ls /sys/class/net/); do "
                    r'addr="$(cat /sys/class/net/$i/address)"; '
                    r'if [[ "$addr" == "$1" ]]; then '
                    r'echo "$i"; '
                    r'fi; '
                    r"done' >> mac2ifname.sh"
                )
                ssh_support.execute_command(self, node_n.ssh_config, command)

                ssh_support.execute_command(
                    self,
                    node_n.ssh_config,
                    'cd ~ && chmod a+x mac2ifname.sh')
                ifname = ssh_support.execute_command(
                    self,
                    node_n.ssh_config,
                    './mac2ifname.sh ' + mac
                )
                i_name = intf.getAttribute("client_id")
                for ipcp in node_n.ipcps:
                    if isinstance(ipcp, mod.ShimEthIPCP):
                        if self.if_id[ipcp] == i_name:
                            ipcp.ifname = ifname
                            if ifname is None or ifname == "":
                                raise Exception("Could not determine name of "
                                                "node %s interface %s"
                                                % (node_n.name, mac))
                            else:
                                logger.debug("Node %s interface %s has name %s."
                                             % (node_n.name, mac, ifname))
                            # comp_id = intf.getAttribute("component_id")
                            # comp_arr = comp_id.split(":")
                            # ipcp.ifname = comp_arr[-1]
                            # xml_ip = intf.getElementsByTagName("ip")
                            # interface.ip = xml_ip[0].getAttribute("address")
