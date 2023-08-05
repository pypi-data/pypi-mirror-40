#!/usr/bin/env bash
# -*- coding: utf-8 -*-

import pytest
import datetime
import unittest
import sys

try:
    import unittest.mock as mock
except ImportError:
    import mock


try:
    import incolumepy.saj_projects as pkg
except ImportError:
    import src.incolumepy.saj_projects as pkg

try:
    pkg.logger.debug("run Python 3")
    from io import StringIO
except ImportError as e:
    pkg.logger.debug('run Python 2'.format(e))
    from cStringIO import StringIO


class TestPackage(unittest.TestCase):

    def test_version_output_0(self):
        expected = '3.22.199'
        with mock.patch('builtins.open', mock.mock_open(read_data=expected)):
            self.assertEqual(expected, pkg.version())

    @mock.patch.object(pkg.datetime, 'datetime')
    def test_version_output_1(self, mock_data):
        expected = '2009.7.5'
        mock_version = mock.Mock(spec=pkg.version)
        mock_version.return_value = expected
        mock_data.now.return_value.strftime.return_value = expected
        self.assertEqual(expected, mock_version(True))

    @mock.patch('datetime.datetime', return_value=pkg.datetime.datetime(2018, 7, 5))
    def test_version_output_2(self, mock_datetime):
        expected = '2018.7.5'
        with mock.patch('builtins.open', mock.mock_open(read_data=expected)):
            with mock.patch('platform.system', return_value='linux'):
                mock_datetime.now.return_value = pkg.datetime.datetime(*expected.split('.'))
                result = pkg.version(True)
                self.assertEqual(expected, result)

            with mock.patch('platform.system', return_value='windows'):
                mock_datetime.now.return_value = pkg.datetime.datetime(*expected.split('.'))
                result = pkg.version(True)
                self.assertEqual(expected, result)

            with mock.patch('platform.system', return_value='mac'):
                mock_datetime.now.return_value = pkg.datetime.datetime(*expected.split('.'))
                result = pkg.version(True)
                self.assertEqual(expected, result)
        pass

    def test_package_output(self):
        expected = f"package '{pkg.__package__}': Version '{pkg.__version__}'"
        self.assertEqual(expected, pkg.package())

    def test_singleton(self):
        pass

    def test_get_logger(self):
        pass

    def test_config_0(self):
        expected = 'Not Set'
        result = pkg.os.environ.get('DEBUSSY', 'Not Set')
        self.assertEqual(expected, result)

        with mock.patch('builtins.open', mock.mock_open(read_data=expected)):
            self.assertEqual(expected, pkg.os.environ.get('DEBUSSY', expected))

    def test_config_1(self):
        expected = 'linux'
        with mock.patch('platform.system', mock.MagicMock(return_value=expected)):
            result = pkg.config()
            self.assertEqual(expected, result.get('system'))
        expected = 'mac'
        with mock.patch('platform.system', mock.MagicMock(return_value=expected)):
            result = pkg.config()
            self.assertEqual(expected, result.get('system'))
        expected = 'windows'
        with mock.patch('platform.system', mock.MagicMock(return_value=expected)):
            result = pkg.config()
            self.assertEqual(expected, result.get('system'))

    def test_config_2(self):
        expected = '%-Y.%-m.%-d'
        with mock.patch('platform.system', mock.MagicMock(return_value='linux')):
            pkg.config()
            result = pkg.os.environ.get('incolumepy_str_version'.upper(), None)
            self.assertEqual(expected, result)
        expected = '%-Y.%-m.%-d'
        with mock.patch('platform.system', mock.MagicMock(return_value='mac')):
            pkg.config()
            result = pkg.os.environ.get('incolumepy_str_version'.upper(), None)
            self.assertEqual(expected, result)
        expected = '%#Y.%#m.%#d'
        with mock.patch('platform.system', mock.MagicMock(return_value='windows')):
            pkg.config()
            result = pkg.os.environ.get('incolumepy_str_version'.upper(), None)
            self.assertEqual(expected, result)

    def test_config_3(self):
        pkg.config()
        self.assertIn('incolumepy_system'.upper(), pkg.os.environ)
        self.assertIn('incolumepy_str_version'.upper(), pkg.os.environ)
        self.assertIn('incolumepy_dir_teste'.upper(), pkg.os.environ)
        pass


if __name__ == '__main__':
    unittest.main()
