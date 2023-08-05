# -*- coding: utf-8 -*-
# pylint: disable=fixme
#
# Copyright (C) 2015-2016: Alignak contrib team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak contrib projet.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
# Copyright (C) 2009-2012:
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    Gregory Starck, g.starck@gmail.com
#    Hartmut Goebel, h.goebel@goebel-consult.de
#
# This file is part of Shinken.
#
# Shinken is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinken is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

"""
This module is an Alignak Poller module that allows to bypass the launch of the check_nrpe process.
"""

import os
import re
import sys
import time
import getopt
import socket
import struct
import binascii
import asyncore
import logging
import signal
import queue
import shlex

from alignak.basemodule import BaseModule
from alignak.misc.common import setproctitle, SIGNALS_TO_NAMES_DICT
from alignak.message import Message

# pylint: disable=wrong-import-position,invalid-name,protected-access
COMMUNICATION_ERRORS = (OSError)

try:
    import OpenSSL
except ImportError as openssl_import_error:
    OpenSSL = None
    SSLError = None
    SSLWantReadOrWrite = None
else:
    SSLError = OpenSSL.SSL.Error
    SSLWantReadOrWrite = (OpenSSL.SSL.WantReadError, OpenSSL.SSL.WantWriteError)

    # consider SSLError's to also be a kind of communication error.
    COMMUNICATION_ERRORS = (OSError, SSLError)
    # effectively, under SSL mode, any TCP reset or such failure
    # will be raised as such an instance of SSLError, which isn't
    # a subclass of IOError nor OSError but we want to catch
    # both so to retry a check in such cases.
    # Look for 'retried' and 'readwrite_error' in the code..

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
for handler in logger.parent.handlers:
    if isinstance(handler, logging.StreamHandler):
        logger.parent.removeHandler(handler)

properties = {
    'daemons': ['poller'],
    'type': 'nrpe_poller',
    'phases': ['running'],

    'external': False,

    # To be a real worker module, we must set this
    'worker_capable': True
}


def get_instance(mod_conf):
    """
    Return a module instance for the modules manager

    :param mod_conf: the module properties as defined globally in this file
    :return:
    """
    logger.info("Give an instance of %s for alias: %s", mod_conf.python_name, mod_conf.module_alias)

    return NrpePoller(mod_conf)


NRPE_DATA_PACKET_SIZE = 1034  # REALLY important .. !


# pylint: disable=too-few-public-methods
class NRPE():
    """
    NRPE protocol
    """
    def __init__(self, host, port, use_ssl, command):
        """
        Build a NRPE query packet
            00-01: NRPE protocol version
            02-03: packet type (01: query, 02: response)
            04-07: CRC32
            08-09: return code of the check if packet type is response
            10-1034: command (nul terminated)
            1035-1036: reserved

        :param host:
        :param port:
        :param use_ssl:
        :param command:
        """
        self.state = 'creation'
        self.host = host
        self.port = port
        self.use_sll = use_ssl
        self.rc = 3
        self.message = ''
        crc = 0

        if not isinstance(command, bytes):
            command = command.encode('utf8')

        # We pack it, then we compute CRC32 of this first query
        try:
            query = struct.pack(">2hIh1024scc", 0x2, 0x1, crc, 0x00, command, b'N', b'D')
        except struct.error:
            logger.error("Packet encoding failed for: %s", str(command))
            return

        # CRC computing as an unsigned integer (compatibility Python 2 / 3)
        crc = binascii.crc32(query) & 0xffffffff

        # we repack with the crc value this time
        self.query = struct.pack(">2hIh1024scc", 0x2, 0x1, crc, 0x0, command, b'N', b'D')

    def read(self, data):
        """
        Read a result and extract return code
        :param data:
        :return:
        """
        # TODO: Not sure to get all the data in one shot.
        # TODO we should buffer it until we get enough to unpack.
        logger.debug("State: %s, received data: %s", self.state, data)
        if self.state in ['received']:
            logger.debug("State: %s, exit: %s, message: %s", self.state, self.rc, self.message)
            return self.rc, self.message

        self.state = 'received'

        try:
            logger.debug("Unpacking data: %s", data)
            p_version, p_type, p_crc, p_rc, p_message = struct.unpack(">2hIh1024s", data)
        except Exception as err:  # bad format...
            logger.error("Packet decoding failed: %s", err)
            self.rc = 3
            self.message = ("Error : cannot unpack output ; "
                            "datalen=%s : err=%s" % (len(data), err))
        else:
            logger.debug("Got: version=%s, type=%s, crc=%s, code=%s, message=%s",
                         p_version, p_type, p_crc, p_rc, p_message)
            self.rc = p_rc
            # the output is padded with \x00 at the end so we remove it.
            self.message = re.sub(b'\x00.*$', b'', p_message)
            # TODO: check crc

        logger.debug("Exit code: %s, message: %s", self.rc, self.message)
        return self.rc, self.message


# pylint: disable=useless-object-inheritance
class NRPEAsyncClient(asyncore.dispatcher, object):
    """
    NRPE client
    """
    # Auto generated identifiers
    _id = 1

    # pylint: disable=too-many-arguments
    def __init__(self, host, port, use_ssl, timeout, unknown_on_timeout, msg,
                 ssl_version, ssl_ciphers_list):
        """

        :param host:
        :param port:
        :param use_ssl:
        :param timeout:
        :param unknown_on_timeout:
        :param msg:
        """
        asyncore.dispatcher.__init__(self)

        # My unique identifier
        cls = self.__class__
        self._id = cls._id
        cls._id += 1

        self.use_ssl = use_ssl
        self.ssl_version = ssl_version
        self.ssl_ciphers_list = ssl_ciphers_list

        self.start_time = time.time()
        self.execution_time = -1
        self.timeout = timeout
        self._rc_on_timeout = 3 if unknown_on_timeout else 2
        self.readwrite_error = False  # there was an error at the tcp level..
        self.exited = False

        # Instantiate our nrpe helper
        self.nrpe = NRPE(host, port, self.use_ssl, msg)
        self.socket = None

        # And now we create a socket for our connection
        try:
            addrinfo = socket.getaddrinfo(host, port)[0]
        except Exception as err:
            self.set_exit(2, "Cannot getaddrinfo: %s" % err)
            return

        self.create_socket(addrinfo[0], socket.SOCK_STREAM)

        if self.use_ssl:
            # The admin want a ssl connection,
            # but there is not openssl lib installed :(
            if OpenSSL is None:
                logger.warning("Python openssl lib is not installed! Cannot use SSL, "
                               "switching back to no-ssl mode; original import error: %s",
                               openssl_import_error)
                self.use_ssl = False
            else:
                self.wrap_ssl(getattr(OpenSSL.SSL, "%s_METHOD" % ssl_version), ssl_ciphers_list)

        address = (host, port)
        logger.debug("%s - connecting: %s", self._id, address)
        try:
            self.connect(address)
        except Exception as err:
            self.set_exit(2, "Cannot connect to %s: %s" % (address, err))
        else:
            self.rc = 3
            self.message = 'Sending request and waiting response...'

    def wrap_ssl(self, ssl_version, ssl_ciphers_list):
        """

        :return:
        """
        logger.debug('%s - SSL connection: %s / %s', self._id, ssl_version, ssl_ciphers_list)
        # One of SSLv2_METHOD, SSLv3_METHOD, SSLv23_METHOD, or TLSv1_METHOD.
        self.context = OpenSSL.SSL.Context(ssl_version)
        # ALL:!MD5:@STRENGTH:@SECLEVEL=0
        self.context.set_cipher_list(ssl_ciphers_list)
        self._socket = self.socket  # keep the bare socket for later shutdown/close
        self.socket = OpenSSL.SSL.Connection(self.context, self.socket)
        self.set_accept_state()

    def close(self):
        """
        Close NRPE connection
        :return:
        """
        if self.socket is None:
            return

        logger.debug("%s - closing...", self._id)

        if self.use_ssl:
            for idx in range(1):
                try:
                    if self.socket.shutdown():
                        break
                except SSLWantReadOrWrite as err:
                    logger.exception('Error on SSL shutdown : %s', err)
                    # pass  # just retry for now
                    # or:
                    # asyncore.poll2(0.5)
                    # but not sure we really need it as the SSL shutdown()
                    # should take care of it.
                except SSLError as err:
                    # on python2.7 I keep getting SSLError instance having no
                    # 'reason' nor 'library' attribute or any other detail.
                    # despite the docs telling the opposite:
                    # https://docs.python.org/2/library/ssl.html#ssl.SSLError
                    details = 'idx=%d library=%s reason=%s : %s' \
                              % (idx, getattr(err, 'library', 'missing'),
                                 getattr(err, 'reason', 'missing'), err)
                    # output the error in debug mode for now.
                    logger.debug('Error on SSL shutdown : %s', details)
                    logger.warning('%s - error on SSL shutdown : %s', self._id, err)
                    # keep retry.
                except Exception as err:
                    logger.warning('SSL shutdown failed: %s', str(err))
            sock = self._socket
        else:
            sock = self.socket

        try:
            # Also always shutdown the underlying socket:
            # pylint: disable=too-many-function-args
            sock.shutdown(socket.SHUT_RDWR)
        except OSError as err:
            logger.debug('socket.shutdown failed: %s', str(err))
        except Exception as err:
            logger.warning('socket.shutdown failed: %s', str(err))

        super(NRPEAsyncClient, self).close()
        self.socket = None
        logger.debug("%s - closed...", self._id)

    def set_exit(self, rc, message):
        """
        Set NRPE request exit information
        :param rc: return code
        :param message: message
        :return:
        """
        logger.debug("%s - socket exit: %s - %s", self._id, rc, message)
        self.exited = True
        self.close()
        self.rc = rc
        self.message = message
        self.execution_time = time.time() - self.start_time
        self.nrpe.state = 'received'
        logger.debug("%s - socket exited: %s - %s", self._id, rc, message)

    def look_for_timeout(self):
        """
        Check if we are in timeout. If so, just bailout and set the correct return code
        from timeout case
        :return:
        """
        now = time.time()
        if now - self.start_time > self.timeout:
            self.set_exit(self._rc_on_timeout,
                          "Error: connection timeout after %d seconds" % self.timeout)

    def handle_connect(self):
        """Handle the socket connection"""
        logger.debug("%s - socket connected", self._id)

    def handle_close(self):
        """Handle the socket close"""
        logger.debug("%s - socket closed", self._id)
        self.close()

    def handle_read(self):
        """
        We got a read from the socket and keep receiving until it has finished.
        Maybe it's just a SSL handshake continuation, if so we continue
        and wait for handshake finish
        :return:
        """
        if self.exited:
            return

        if self.is_done():
            return

        try:
            self._handle_read()
        except COMMUNICATION_ERRORS as err:
            self.readwrite_error = True
            self.set_exit(2, "Error on read: %s" % err)

    def _handle_read(self):
        """
        Read received data
        :return:
        """
        try:
            buffer = self.recv(NRPE_DATA_PACKET_SIZE)
        except SSLWantReadOrWrite:
            # if we are in ssl, there can be a handshake
            # problem: we can't talk until we finished it.
            try:
                self.socket.do_handshake()
            except SSLWantReadOrWrite:
                pass
            return
        else:
            # Maybe we got nothing from the server (it refused our IP,
            # or our arguments...)
            if buffer:
                rc, message = self.nrpe.read(buffer)
                logger.debug("Got, exit code: %s, message: %s", self.rc, self.message)
            else:
                rc = 2
                message = "Error: Empty response from the NRPE server. Are we blacklisted ?"

        self.set_exit(rc, message)

    def writable(self):
        """
        Did we finished our job?
        :return:
        """
        return not self.exited and not self.is_done() and self.nrpe.query

    def handle_write(self):
        """
        We can write to the socket. If we are in the ssl handshake phase we just continue
        and return. If we finished, we can write our query
        :return:
        """
        if self.exited:
            return

        try:
            self._handle_write()
        except COMMUNICATION_ERRORS as err:
            self.readwrite_error = True
            self.set_exit(2, 'Error on write: %s' % err)

    def _handle_write(self):
        """
        Write data
        :return:
        """
        try:
            sent = self.send(self.nrpe.query)
        except SSLWantReadOrWrite:
            # SSL write/send can require a read ! yes ;)
            try:
                self.socket.do_handshake()
            except SSLWantReadOrWrite:
                # still not finished, we continue
                pass
        else:
            # Maybe we did not sent all our query so we bufferize it
            self.nrpe.query = self.nrpe.query[sent:]

    def is_done(self):
        """
        NRPE check finished
        :return:
        """
        return self.nrpe.state == 'received'

    def handle_error(self):
        """
        Handle an error
        :return:
        """
        _, err, _ = sys.exc_info()
        logger.debug("%s - socket error: %s", self._id, err)
        self.set_exit(2, "Error: %s" % err)


def parse_args(cmd_args):
    """
    Parse check_nrpe arguments
    :param cmd_args:
    :return:
    """
    # Default params
    host = None
    command = None
    port = 5666
    unknown_on_timeout = False
    timeout = 10
    use_ssl = True
    add_args = []

    # Manage the options
    # NRPE Plugin for Nagios
    # Copyright (c) 1999-2008 Ethan Galstad (nagios@nagios.org)
    # Version: 2.15
    # Last Modified: 09-06-2013
    # License: GPL v2 with exemptions (-l for more info)

    # Usage: check_nrpe -H <host> [ -b <bindaddr> ]
    #                   [-4] [-6] [-n] [-u]
    #                   [-p <port>] [-t <timeout>]
    #                   [-c <command>] [-a <arglist...>]

    # Options:
    #  -n         = Do no use SSL
    #  -u         = Make socket timeouts return an UNKNOWN state instead of CRITICAL
    #  <host>     = The address of the host running the NRPE daemon
    #  <bindaddr> = bind to local address
    #  -4         = user ipv4 only
    #  -6         = user ipv6 only
    #  [port]     = The port on which the daemon is running (default=5666)
    #  [timeout]  = Number of seconds before connection times out (default=10)
    #  [command]  = The name of the command that the remote daemon should run
    #  [arglist]  = Optional arguments that should be passed to the command.  Multiple
    #               arguments should be separated by a space.  If provided, this must be
    #               the last option supplied on the command line.

    # Note:
    # This plugin requires that you have the NRPE daemon running on the remote host.
    # You must also have configured the daemon to associate a specific plugin command
    # with the [command] option you are specifying here.  Upon receipt of the
    # [command] argument, the NRPE daemon will run the appropriate plugin command and
    # send the plugin output and return code back to *this* plugin.  This allows you
    # to execute plugins on remote hosts and 'fake' the results to make Nagios think
    # the plugin is being run locally.

    logger.debug("Received arguments: %s", cmd_args)
    try:
        opts, args = getopt.getopt(cmd_args, "H::p::nut::c::a::", [])
    except getopt.GetoptError as err:
        # If we got problem, bail out - say host is None
        logger.warning("Could not parse command parameters: %s", cmd_args)
        logger.warning("Error is: %s", str(err))
        return None, port, unknown_on_timeout, command, timeout, use_ssl, add_args

    logger.debug("Parsing arguments: opts = %s, args = %s", opts, args)
    try:
        for o, a in opts:
            if o == "-H":
                host = a
            elif o == "-p":
                port = int(a)
            elif o == "-c":
                command = a
            elif o == '-t':
                timeout = int(a)
            elif o == '-u':
                unknown_on_timeout = True
            elif o == '-n':
                use_ssl = False
            elif o == '-a':
                # Here we got a, but also all 'args'
                add_args.append(a)
                add_args.extend(args)
    except ValueError as err:
        # If we got problem, bail out - say host is None
        logger.error("Could not parse command parameters: %s", cmd_args)
        logger.error("Check the module and command configuration (macros, ...)")
        return None, port, unknown_on_timeout, command, timeout, use_ssl, add_args

    return host, port, unknown_on_timeout, command, timeout, use_ssl, add_args


class NrpePoller(BaseModule):
    """
    NRPE Poller module main class
    """
    # Auto generated identifiers
    _worker_ids = {}

    def __init__(self, mod_conf):
        """
        Module initialization

        mod_conf is a dictionary that contains:
        - all the variables declared in the module configuration file
        - a 'properties' value that is the module properties as defined globally in this file

        :param mod_conf: module configuration file as a dictionary
        """
        BaseModule.__init__(self, mod_conf)

        # Set our own identifier
        cls = self.__class__
        self.module_name = 'nrpe-booster'
        if self.module_name not in cls._worker_ids:
            cls._worker_ids[self.module_name] = 1
        self._id = '%s_%d' % (self.module_name, cls._worker_ids[self.module_name])
        cls._worker_ids[self.module_name] += 1

        # pylint: disable=global-statement
        global logger
        logger = logging.getLogger('alignak.module.%s' % self.alias)
        if getattr(mod_conf, 'log_level', logging.INFO) in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            logger.setLevel(getattr(mod_conf, 'log_level'))

        logger.debug("inner properties: %s", self.__dict__)
        logger.debug("received configuration: %s", mod_conf.__dict__)

        try:
            self.period_stats = int(getattr(mod_conf, 'period_stats', '10'))
        except ValueError:
            self.period_stats = 10
        logger.info("configuration, loop count period for statistics: %d", self.period_stats)

        try:
            self.max_plugins_output_length = int(getattr(
                mod_conf, 'max_plugins_output_length', '8192'))
        except ValueError:
            self.max_plugins_output_length = 8192
        logger.info("configuration, maximum output length: %d", self.max_plugins_output_length)

        # SSL configuration
        self.ssl_method = getattr(mod_conf, 'ssl_ciphers_list', 'SSLv23')
        if self.ssl_method not in ['SSLv2', 'SSLv3', 'SSLv23', 'TLSv1']:
            logger.error("SSL configured method is unknown: %s. SSL will not be enabled...",
                         self.ssl_method)
        self.ssl_ciphers_list = getattr(mod_conf, 'ssl_ciphers_list',
                                        'ALL:!MD5:@STRENGTH:@SECLEVEL=0')

        self.checks = []

        self.returns_queue = None
        self.actions_queue = None
        self.t_each_loop = None

        self._idletime = 0
        self.actions_got = 0
        self.actions_launched = 0
        self.actions_retried = 0
        self.actions_failed = 0
        self.actions_finished = 0

        self.interrupted = False

        self.i_am_dying = False

    def init(self):
        """
        Called by the poller to initialize the module
        :return: True to inform ModuleManager of a correct initialization
        """
        logger.info("NRPE poller module %s initialized for %s", self._id, self.loaded_into)
        self.i_am_dying = False

        return True

    def quit(self):
        """
        Called by the poller to exit the module
        :return: None
        """
        logger.info("NRPE poller module %s exited", self._id)

    def do_loop_turn(self):
        pass

    def got_new_check(self, check):
        """
        Add a new check to execute
        :param check: alignak.Check
        :return:
        """
        check.retried = 0
        logger.debug("Got a new check: %s", check.__dict__)
        self.checks.append(check)
        self.actions_got += 1

    def get_new_checks(self):
        """

        :return:
        """
        while True:
            try:
                msg = self.actions_queue.get_nowait()
            except queue.Full:
                logger.warning("Worker actions queue is full!")
                return
            except queue.Empty:
                self._idletime += 1
                return
            else:
                if msg:
                    self.got_new_check(msg.get_data())

    def launch_new_checks(self):
        # pylint: disable=too-many-locals
        """
        Launch the new received checks

        A check is a dictionary:
        {'log_actions': False, 'exit_status': 3, 'passive_check': False,
        'creation_time': 1546333142.255722, 'reactionner_tag': u'None', 's_time': 0.0,
        'my_scheduler': '7edeba2b-4874-4680-967a-7ab0c94a702d',
        'uuid': u'a657edb3-b077-482b-894a-879251efa40e', 'check_time': 0,
        'long_output': u'', 'wait_time': 0.001, 'state': 0, 'internal': False, 'u_time': 0.0,
        'env': {}, 'freshness_expiry_check': False, 'depend_on_me': [], 'type': u'',
        'status': u'queued', 'retried': 0, 'execution_time': 0.0, 't_to_go': 1546333437,
        'module_type': u'nrpe-booster', 'last_poll': 0, '_in_timeout': False,
        'ref_type': u'service', 'dependency_check': False, 'my_worker': u'nrpe-booster_1',
        'ref': u'344df95f-985e-43cd-adfa-deffec53bcbc', 'depend_on': [], 'is_a': u'check',
        'poller_tag': u'nrpe', 'command': u'/usr/lib/nagios/plugins/check_nrpe -H 10.0.2.22
        -t 10 -u -n -c check_users', 'timeout': 60, 'output': u'', 'perf_data': u''}
        :return:
        """
        for check in self.checks:
            now = time.time()
            # Both status may have been used... ascending compatibility!
            if check.status not in ['queue', 'queued']:
                continue

            check.con = None

            # Ok we launch it
            check.status = 'launched'
            check.check_time = now

            # We want the args of the commands so we parse it like a shell
            # shlex wants str only
            try:
                clean_command = shlex.split(check.command.encode('utf8', 'ignore'))
            except AttributeError:
                clean_command = shlex.split(check.command)

            # Set an error so we will quit this check
            host = None
            command = None

            # If the command seems good
            if len(clean_command) > 1:
                # we do not want the first member, check_nrpe thing
                args = parse_args(clean_command[1:])
                (host, port, unknown_on_timeout, command, timeout, use_ssl, add_args) = args
                logger.debug("Parsed arguments: %s / %s / %s / %s / %s / %s / %s",
                             host, port, unknown_on_timeout, command, timeout, use_ssl, add_args)

            # If we do not have the good args, we bail out for this check
            if host is None:
                check.status = 'done'
                check.exit_status = 2
                check.get_outputs('Error: the host parameter is not correct.',
                                  self.max_plugins_output_length)
                check.execution_time = 0
                continue

            # if no command is specified, check_nrpe
            # sends _NRPE_CHECK as the default command.
            if command is None:
                command = '_NRPE_CHECK'

            # Ok we are good, we go on
            total_args = [command]
            total_args.extend(add_args)
            cmd = r'!'.join(total_args)

            log_function = logger.debug
            if 'ALIGNAK_LOG_ACTIONS' in os.environ:
                if os.environ['ALIGNAK_LOG_ACTIONS'] == 'WARNING':
                    log_function = logger.warning
                else:
                    log_function = logger.info
            log_function("Launch NRPE check: %s", cmd)

            check.con = NRPEAsyncClient(host, port, use_ssl, timeout, unknown_on_timeout,
                                        cmd, self.ssl_method, self.ssl_ciphers_list)

            self._idletime = 0
            self.actions_launched += 1

    def manage_finished_checks(self):
        """
        Check the status of the checks
        :return:
        """
        # First look if launched checks are in timeout
        to_del = []
        for check in self.checks:
            if check.status not in ['launched']:
                continue

            try:
                check.con.look_for_timeout()
            except Exception as err:
                logger.info("manage_finished_checks - error: %s, connection: %s, check: %s",
                            err, check.con._id, check)
                self.actions_failed += 1

        # Now we look for finished checks
        to_del = []
        logger.debug("--- %d checks", len(self.checks))
        for check in self.checks:
            # First manage check in error, bad formed
            if check.status == 'done':
                self.actions_finished += 1
                to_del.append(check)

                try:
                    msg = Message(_type='Done', data=check, source=self._id)
                    logger.debug("Queuing message: %s", msg)
                    self.returns_queue.put_nowait(msg)
                except Exception as exp:  # pylint: disable=broad-except
                    logger.error("Failed putting messages in returns queue: %s", str(exp))

            # Then we check for finished or timed out checks
            elif check.status == 'launched' and check.con.is_done():
                # unlink our object from the original check,
                # this might be necessary to allow the check to be again
                # serializable..
                con = check.con
                del check.con

                if con.readwrite_error and check.retried < 2:
                    logger.warning("%s: Got an I/O error (%s), retrying 1 more time... "
                                   "Current try is %d", check.command, con.message, check.retried)
                    check.retried += 1
                    check.status = 'queued'
                    continue

                if check.retried:
                    logger.info('%s: retried check :)', check.command)

                check.status = 'done'
                check.exit_status = con.rc
                try:
                    con.message = con.message.decode("utf-8")
                except AttributeError:
                    pass

                check.get_outputs(con.message, self.max_plugins_output_length)
                check.execution_time = con.execution_time

                self.actions_finished += 1
                to_del.append(check)

                try:
                    msg = Message(_type='Done', data=check, source=self._id)
                    logger.debug("Queuing message: %s", msg)
                    self.returns_queue.put_nowait(msg)
                except Exception as exp:  # pylint: disable=broad-except
                    logger.error("Failed putting messages in returns queue: %s", str(exp))

        # And delete finished checks
        for check in to_del:
            self.checks.remove(check)
        if self.checks:
            logger.debug("--- %d still launched checks", len(self.checks))

    def work(self, actions_queue, returns_queue, control_queue):
        """
        Wrapper function for work in order to catch the exception
        to see the real work, look at do_work
        """
        try:
            logger.info("[%s] (pid=%d) starting my job...", self._id, os.getpid())
            self.do_work(actions_queue, returns_queue, control_queue)
            logger.info("[%s] (pid=%d) stopped", self._id, os.getpid())
        # Catch any exception, log the exception and exit anyway
        except Exception as exp:  # pragma: no cover, this should never happen indeed ;)
            logger.error("[%s] exited with an unmanaged exception : %s", self._id, str(exp))
            logger.exception(exp)

    def do_work(self, actions_queue, returns_queue, control_queue):
        """

        :param s: global queue
        :param returns_queue: queue of our manager
        :param c: control queue for the worker
        :return:
        """
        # restore default signal handler for the workers:
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

        setproctitle("alignak-%s worker %s" % (self.loaded_into, self._id))

        self.returns_queue = returns_queue
        self.actions_queue = actions_queue
        self.t_each_loop = time.time()

        timeout = 1.0
        counter = 1

        while True:
            begin = time.time()
            logger.debug("[%s] loop begin: %s", self._id, begin)

            try:
                # We check if all new things in connections
                # NB : using poll2 instead of poll (poll1 is with select
                # call that is limited to 1024 connexions, poll2 is ... poll).
                # asyncore.poll2(1)
                # asyncore.loop(1.0, use_poll=True)
                # asyncore.loop(timeout)
                asyncore.loop(timeout, use_poll=True)
            except socket.error as err:
                logger.debug('Socket polling error: %s / %s', sys.exc_info(), err)
            except Exception as err:
                self.actions_failed += 1
                logger.info('Socket polling error: %s / %s', sys.exc_info(), err)

            # If we are dying (big problem!) we do not
            # take new jobs, we just finished the current one
            if not self.i_am_dying:
                # REF: doc/shinken-action-queues.png (3)
                self.get_new_checks()
                # REF: doc/shinken-action-queues.png (4)
                self.launch_new_checks()

            # REF: doc/shinken-action-queues.png (5)
            self.manage_finished_checks()

            # Maybe someone asked us to die, if so, do it :)
            if self.interrupted:
                logger.info("I die because someone asked ;)")
                break

            # Now get order from master, if any...
            if control_queue:
                try:
                    control_message = control_queue.get_nowait()
                    logger.info("[%s] Got a message: %s", self._id, control_message)
                    if control_message.get_type() == 'Die':
                        logger.info("[%s] The master said we must die... :(", self._id)
                        break
                except queue.Full:
                    logger.warning("Worker control queue is full")
                except queue.Empty:
                    pass
                except Exception as exp:  # pylint: disable=broad-except
                    logger.error("Exception when getting master orders: %s. ", str(exp))

            timeout -= time.time() - begin
            if timeout < 0:
                timeout = 1.0
            # time.sleep(0.5)

            counter += 1
            log_function = logger.debug
            if counter > self.period_stats:
                # Periodically, sends our statistics and raise a log
                if 'ALIGNAK_LOG_ACTIONS' in os.environ:
                    if os.environ['ALIGNAK_LOG_ACTIONS'] == 'WARNING':
                        log_function = logger.warning
                    else:
                        log_function = logger.info
                data = {
                    'idle': self._idletime,
                    'got': self.actions_got,
                    'launched': self.actions_launched,
                    'failed': self.actions_failed,
                    'finished': self.actions_finished
                }
                msg = Message(_type='Stats', data=data, source=self._id)
                self.returns_queue.put_nowait(msg)
                counter = 1

            log_function("+++ loop end: timeout = %s, idle: %s, checks: %d, "
                         "actions (got: %d, launched: %d, finished: %d, failed: %d)",
                         timeout, self._idletime, len(self.checks),
                         self.actions_got, self.actions_launched,
                         self.actions_finished, self.actions_failed)
