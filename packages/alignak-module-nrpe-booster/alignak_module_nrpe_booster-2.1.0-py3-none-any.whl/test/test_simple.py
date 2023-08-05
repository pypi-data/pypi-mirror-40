#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak.
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

import os
import re
import time
import logging

from builtins import range

from multiprocessing import Queue, Manager
from .alignak_test import AlignakTest
from alignak.check import Check

try:
    import unittest2 as unittest
except ImportError:
    import unittest


from alignak.daemons.pollerdaemon import Poller
from alignak.modulesmanager import ModulesManager
from alignak.objects.module import Module
from alignak.message import Message

import alignak_module_nrpe_booster

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NrpePollerTestMixin(object):

    def setUp(self):
        super(NrpePollerTestMixin, self).setUp()
        logger.setLevel(logging.DEBUG)

        # Do not activate more logs
        if 'ALIGNAK_LOG_ACTIONS' in os.environ:
            del os.environ['ALIGNAK_LOG_ACTIONS']

    def _setup_nrpe(self):
        # Create an Alignak module
        mod = Module({
            'module_alias': 'nrpe-booster',
            'module_types': 'nrpe-booster',
            'python_name': 'alignak_module_nrpe_booster'
        })

        # Create the modules manager for a daemon type
        args = {
            'env_file': self.env_filename, 'daemon_name': 'poller-master',
        }
        self._poller_daemon = Poller(**args)

        self.modulemanager = ModulesManager(self._poller_daemon)
        # Load and initialize the modules
        self.modulemanager.load_and_init([mod])
        my_module = self.modulemanager.instances[0]
        return my_module


@unittest.skipIf(os.name == 'nt', "NRPE poller do not run with Windows")
class TestNrpePoller(NrpePollerTestMixin, AlignakTest):
    def test_nrpe_poller(self):
        """

        :return:
        """
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/alignak.cfg', 'cfg/alignak.ini')
        self.assertTrue(self.conf_is_correct)

        my_module = self._setup_nrpe()

        manager = Manager()
        to_queue = manager.Queue()
        from_queue = manager.Queue()
        control_queue = Queue()

        # We prepare a check in the to_queue
        data = {
            'is_a': 'check',
            'status': 'queued',
            'command': "$USER1$/check_nrpe -H localhost33  -n -u -t 5 -c check_load3 -a 20",
            'timeout': 10,
            'poller_tag': None,
            't_to_go': time.time(),
            'ref': None,
        }
        c = Check(data)

        Message._id = 0
        msg = Message(_type='Do', data=c)
        print(msg)
        to_queue.put(msg)

        # The worker will read a message by loop. We want it to do minimum 10 loops,
        # so we fake a message, and the second message is a real exit one
        _run = Message('Continue', source="Me")
        _die = Message('Die', source="Me")
        for _ in range(1, 12):
            control_queue.put(_run)
        control_queue.put(_die)

        # Call module working ...
        self.clear_logs()
        my_module.work(to_queue, from_queue, control_queue)

        # Got a check restul
        msg = from_queue.get()
        self.assertIsInstance(msg, Message)
        self.assertEqual(msg.get_type(), 'Done')
        chk = msg.get_data()
        self.assertEqual('done', chk.status)
        self.assertEqual(2, chk.exit_status)

        # Got a statistics report
        msg = from_queue.get()
        self.assertIsInstance(msg, Message)
        self.assertEqual(msg.get_type(), 'Stats')
        stats = msg.get_data()
        # {'idle': 9, 'got': 1, 'launched': 1, 'failed': 0, 'finished': 1}
        print(stats)
        self.assertEqual(stats['idle'], 9)
        self.assertEqual(stats['got'], 1)
        self.assertEqual(stats['launched'], 1)
        self.assertEqual(stats['failed'], 0)
        self.assertEqual(stats['finished'], 1)

        self.show_logs()
        self.assert_log_match("starting my job...", 0)
        for idx in range(1, 12):
            self.assert_log_match("Got a message: Me - 1, type: Continue, data: None", idx)
        self.assert_log_match("Got a message: Me - 2, type: Die, data: None", 12)
        self.assert_log_match("The master said we must die...", 13)
        self.assert_log_match("stopped", 14)
