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
import paramiko
import re
import time

from paramiko.ssh_exception import *

import rumba.log as log

# Fix input reordering
from rumba.model import Executor

try:
    import builtins  # Only in Python 3

    def input(prompt=''):
        log.flush_log()
        return builtins.input(prompt)
except ImportError:  # We are in Python 2
    import __builtin__

    def input(prompt=''):
        log.flush_log()
        return __builtin__.raw_input(prompt)


logger = log.get_logger(__name__)


class SSHException(Exception):
    pass


def get_ssh_client():
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    return ssh_client


def _print_stream(stream):
        o = str(stream.read()).strip('b')
        o = o.strip('\'\"')
        o = o.rstrip()
        o = re.sub(r'(\\n)*$', '', o)
        if o != "":
            o_array = o.split('\\n')
            for oi in o_array:
                logger.debug(oi)
        else:
            o_array = []
        return '\n'.join(o_array)


def ssh_connect(hostname, port, username, password, time_out, proxy_server):
    logger.debug('Trying to open a connection towards node %s.' % hostname)
    retry = 0
    max_retries = 10
    while retry < max_retries:
        time.sleep(retry * 5)

        try:
            proxy_client = None
            if proxy_server is not None:
                proxy_client = get_ssh_client()
                # Assume port 22 for the proxy server for now
                proxy_client.connect(proxy_server, 22, username, password,
                                     look_for_keys=True, timeout=time_out)

                trans = proxy_client.get_transport()
                trans.set_keepalive(30)
                proxy = trans.open_channel('direct-tcpip',
                                           (hostname, port), ('127.0.0.1', 0))
            else:
                proxy = None

            ssh_client = get_ssh_client()

            ssh_client.connect(hostname, port, username, password,
                               look_for_keys=True, timeout=time_out, sock=proxy)
            return ssh_client, proxy_client
        except paramiko.ssh_exception.BadHostKeyException:
            retry += 1
            logger.error(hostname + ' has a mismatching entry in ' +
                         '~/.ssh/known_hosts')
            logger.error('If you are sure this is not a man in the ' +
                         'middle attack, edit that file to remove the ' +
                         'entry and then hit return to try again.')
            input('Key mismatch detected. Press ENTER when ready.')
        except (paramiko.ssh_exception.SSHException, EOFError):
            retry += 1
            logger.error('Failed to connect to host, retrying: ' +
                         str(retry) + '/' + str(max_retries) + ' retries')
    if retry == max_retries:
        raise SSHException('Failed to connect to host')

def ssh_connect_check(ssh_config, testbed, time_out, force_reconnect=False):
    if ssh_config.client is None or \
       not ssh_config.client.get_transport().is_active or force_reconnect:
        client, proxy_client = ssh_connect(ssh_config.hostname, ssh_config.port,
                                           testbed.username, testbed.password,
                                           time_out, ssh_config.proxy_server)
        ssh_config.client = client
        ssh_config.proxy_client = proxy_client

def ssh_chan(ssh_config, testbed, time_out):
    retry = 0
    max_retries = 2
    while retry < max_retries:
        try:
            ssh_config.client.get_transport().set_keepalive(30)
            chan = ssh_config.client.get_transport().open_session()
            return chan
        except paramiko.ssh_exception.SSHException as e:
            if str(e) == 'No existing session' or \
               str(e) == 'SSH session not active':
                logger.debug('Failed to open transport: ' + str(e))
                retry += 1
                logger.debug('Trying to reconnect: ' +
                             str(retry) + '/' + str(max_retries) + ' retries.')
                ssh_connect_check(ssh_config, testbed, time_out,
                                  force_reconnect=True)
            else:
                raise e

    if retry == max_retries:
        raise SSHException('Unable to re-establish SSH connection.')

def ssh_sftp(ssh_config, testbed):
    chan = ssh_chan(ssh_config, testbed, None)
    chan.invoke_subsystem("sftp")
    return paramiko.sftp_client.SFTPClient(chan)

def execute_commands(testbed, ssh_config, commands, time_out=3):
    """
    Remote execution of a list of shell command on hostname. By
    default this function will exit (timeout) after 3 seconds.

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param commands: *nix shell command
    @param time_out: time_out value in seconds, error will be generated if
    no result received in given number of seconds, the value None can
    be used when no timeout is needed
    """

    ssh_connect_check(ssh_config, testbed, time_out)
    o = ""
    for command in commands:
        logger.debug("%s@%s:%s >> %s" % (testbed.username,
                                         ssh_config.hostname,
                                         ssh_config.port,
                                         command))
        envars = '. /etc/profile;'
        command = envars + ' ' + command

        chan = ssh_chan(ssh_config, testbed, time_out)

        stdout = chan.makefile()
        stderr = chan.makefile_stderr()
        try:
            chan.exec_command(command)
        except paramiko.ssh_exception.SSHException as e:
            raise SSHException('Failed to execute command')
        o = _print_stream(stdout)
        if chan.recv_exit_status() != 0:
            # Get ready for printing stdout and stderr
            if o != "":
                list_print = ['**** STDOUT:']
                list_print += o.split('\\n')
            else:
                list_print = []
            e = _print_stream(stderr)
            if e != "":
                list_print.append('**** STDERR:')
                list_print += e.split('\\n')
            raise SSHException('A remote command returned an error. '
                               'Output:\n\n\t' +
                               '\n\t'.join(list_print) + '\n')
    return o


def execute_command(testbed, ssh_config, command, time_out=3):
    """
    Remote execution of a list of shell command on hostname. By
    default this function will exit (timeout) after 3 seconds.

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param command: *nix shell command
    @param time_out: time_out value in seconds, error will be generated if
    no result received in given number of seconds, the value None can
    be used when no timeout is needed

    @return: stdout resulting from the command
    """
    o = execute_commands(testbed, ssh_config, [command], time_out)
    if o is not None:
        return o


def write_text_to_file(testbed, ssh_config, text, file_name):
    """
    Write a string to a given remote file.
    Overwrite the complete file if it already exists!

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param text: string to be written in file
    @param file_name: file name (including full path) on the host
    """

    ssh_connect_check(ssh_config, testbed, time_out=None)

    cmd = "touch " + file_name + "; chmod a+rwx " + file_name

    try:
        stdin, stdout, stderr = ssh_config.client.exec_command(cmd)
        del stdin, stdout
        err = str(stderr.read()).strip('b\'\"\\n')
        if err != "":
            logger.error(err)

        sftp_client = ssh_sftp(ssh_config, testbed)
        remote_file = sftp_client.open(file_name, 'w')

        remote_file.write(text)
        remote_file.close()

    except SSHException as e:
        raise SSHException('Failed to write text to remote file')


def copy_files_to_testbed(testbed, ssh_config, paths, destination):
    """
    Copies local files to a remote node.

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param paths: source paths (local) as an iterable
    @param destination: destination folder name (remote)
    """
    if destination is not '' and not destination.endswith('/'):
        destination = destination + '/'

    ssh_connect_check(ssh_config, testbed, time_out=None)

    try:
        sftp_client = ssh_sftp(ssh_config, testbed)

        for path in paths:
            file_name = os.path.basename(path)
            dest_file = destination + file_name
            logger.debug("Copying %s to %s@%s:%s path %s" % (
                path,
                testbed.username,
                ssh_config.hostname,
                ssh_config.port,
                dest_file))
            sftp_client.put(path, dest_file)

    except Exception as e:
        raise SSHException('Failed to copy files to testbed')


def copy_file_to_testbed(testbed, ssh_config, path, destination):
    """
    Copies a local file to a remote node.

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param path: source path (local)
    @param destination: destination folder name (remote)
    """
    copy_files_to_testbed(testbed, ssh_config, [path], destination)


def copy_files_from_testbed(testbed, ssh_config, paths,
                            destination, sudo=False):
    """
    Copies local files to a remote node.

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param paths: source paths (remote) as an iterable
    @param destination: destination folder name (local)
    @param sudo: if path to copy requires root access, should be set to true
    """
    if destination is not '' and not destination.endswith('/'):
        destination = destination + '/'

    if sudo:
        cmd = 'chmod a+rw %s' % (" ".join(paths))
        if ssh_config.username != 'root':
            cmd = "sudo %s" % cmd
        execute_command(testbed, ssh_config, cmd)

    ssh_connect_check(ssh_config, testbed, time_out=None)

    try:
        sftp_client = ssh_sftp(ssh_config, testbed)

        for path in paths:
            file_name = os.path.basename(path)
            dest_file = destination + file_name
            logger.debug("Copying %s@%s:%s path %s to %s" % (
                testbed.username,
                ssh_config.hostname,
                ssh_config.port,
                path,
                dest_file))
            sftp_client.get(path, dest_file)

    except Exception as e:
        raise SSHException('Failed to copy files from testbed', e)


def copy_file_from_testbed(testbed, ssh_config, path,
                           destination, sudo=False):
    """
    Copies a local file to a remote node.

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param path: source path (remote)
    @param destination: destination folder name (local)
    @param sudo: if path to copy requires root access, should be set to true
    """
    copy_files_from_testbed(testbed, ssh_config, [path], destination, sudo)


def setup_vlans(testbed, node, vlans):
    """
    Gets the interface (ethx) to link mapping

    @param testbed: testbed info
    @param node: the node to create the VLAN on
    @param vlans: list of lists of VLAN id to interface
    """
    if testbed.username == 'root':
        def sudo(s):
            return s
    else:
        def sudo(s):
            return "sudo sh -c '" + s + "'"

    cmds = [sudo("for file in $(ls -d /etc/udev/rules.d/*); do rm $file; " +
                 "ln -s /dev/null $file; done")]

    for item in vlans:
        args = {'ifname': str(item[0]), 'vlan': str(item[1])}
        cmds += [sudo("ip link add link %(ifname)s name "
                      "%(ifname)s.%(vlan)s type vlan id %(vlan)s" % args),
                 sudo("ip link set dev %(ifname)s.%(vlan)s up" % args)]
        if testbed.flags['no_vlan_offload']:
            cmds += [sudo("ethtool -K %(ifname)s rxvlan off" % args),
                     sudo("ethtool -K %(ifname)s txvlan off" % args)]

    logger.info('Setting up VLANs for node %s', node.name)

    execute_commands(testbed, node.ssh_config, cmds)


def aptitude_install(testbed, node, packages):
    """
    Installs packages through aptitude

    @param testbed: testbed info
    @param node: the node to install the packages on
    @param packages: list of packages
    """

    if testbed.username == 'root':
        def sudo(s):
            return s
    else:
        def sudo(s):
            return 'sudo ' + s

    package_install = "apt-get install "
    for package in packages:
        package_install += package + " "
    package_install += "--yes"

    cmds = [sudo("sh -c 'while fuser /var/lib/dpkg/lock > /dev/null 2>&1; " +
                 "do sleep 1; echo \"Waiting for dpkg...\"; done'"),
            "while ! " + sudo("apt-get update") + "; do sleep 1; done",
            "while ! " + sudo(package_install) + "; do sleep 1; done"]

    execute_commands(testbed, node.ssh_config, cmds, time_out=None)

def set_http_proxy(testbed, node, proxy):
    """
    Sets a system-wide HTTP proxy for a node.

    @param testbed: testbed info
    @param node: the node
    """

    proxies = []
    proxies.append('export http_proxy="' + proxy + '"')
    proxies.append('export https_proxy="' + proxy + '"')

    cmds = []
    for line in proxies:
        cmds.append('echo \''+ line + '\' | sudo tee --append /etc/profile')

    execute_commands(testbed, node.ssh_config, cmds, time_out=None)
