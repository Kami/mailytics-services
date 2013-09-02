#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import subprocess

from glob import glob
from os.path import splitext, basename, join as pjoin
from unittest import TextTestRunner, TestLoader

from setuptools import setup
from distutils.core import Command

sys.path.insert(0, pjoin(os.path.dirname(__file__)))
from test_utils.process_runners import TCPProcessRunner

THIS_DIR = os.path.abspath(os.path.split(__file__)[0])
TEST_PATHS = ['tests']


class TestCommand(Command):
    description = 'run test suite'
    user_options = []

    def initialize_options(self):
        FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
        logging.basicConfig(format=FORMAT)

        sys.path.insert(0, THIS_DIR)
        for test_path in TEST_PATHS:
            sys.path.insert(0, pjoin(THIS_DIR, test_path))

        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        self._flush_db()
        self._run_mock_servers()

        status = self._run_tests()
        sys.exit(status)

    def _run_tests(self):
        testfiles = []
        for test_path in TEST_PATHS:
            for t in glob(pjoin(self._dir, test_path, 'test_*.py')):
                testfiles.append('.'.join(
                    [test_path.replace('/', '.'), splitext(basename(t))[0]]))

        tests = TestLoader().loadTestsFromNames(testfiles)

        t = TextTestRunner(verbosity=2)
        res = t.run(tests)
        return not res.wasSuccessful()

    def _flush_db(self):
        cwd = os.getcwd()
        args = ['scripts/flush-db.sh']
        subprocess.Popen(args, shell=True, cwd=cwd, stdout=sys.stdout,
                         stderr=sys.stdout)
        time.sleep(0.5)

    def _run_mock_servers(self):
        #set_server = TCPProcessRunner()
        script = pjoin(THIS_DIR, 'bin/token-storage-get-server')
        args = [script, '--port=8888']
        wait_for_address = ('127.0.0.1', 8888)
        get_server = TCPProcessRunner(args=args,
                                      wait_for_address=wait_for_address,
                                      log_path='get_server.log')
        get_server.setUp()

        script = pjoin(THIS_DIR, 'bin/token-storage-set-server')
        args = [script, '--port=9999']
        wait_for_address = ('127.0.0.1', 9999)
        set_server = TCPProcessRunner(args=args,
                                      wait_for_address=wait_for_address,
                                      log_path='set_server.log')
        set_server.setUp()


setup(
    name='',
    version='',
    description='',
    #long_description=open('README.rst').read() + '\n\n' +
    #open('CHANGES.rst').read(),
    author='Tomaz Muraus',
    author_email='tomaz+pypi@tomaz.me',
    #packages=['yubico_client'],
    #provides=['yubico_client'],
    cmdclass={
        'test': TestCommand,
    },
)
