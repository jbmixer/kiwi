from nose.tools import *
from mock import patch

import mock

import nose_helper

from collections import namedtuple
from kiwi.system_size import SystemSize


class TestSystemSize(object):
    def setup(self):
        self.size = SystemSize('source_dir')

    def test_customize_ext(self):
        self.size.accumulate_files = mock.Mock(
            return_value=10000
        )
        assert self.size.customize(42, 'ext3') == 67

    def test_customize_btrfs(self):
        assert self.size.customize(42, 'btrfs') == 63

    def test_customize_xfs(self):
        assert self.size.customize(42, 'xfs') == 50

    @patch('kiwi.system_size.Command.run')
    def test_accumulate_mbyte_file_sizes(self, mock_command):
        self.size.accumulate_mbyte_file_sizes()
        mock_command.assert_called_once_with(
            ['du', '-s', '--apparent-size', '--block-size', '1', 'source_dir']
        )

    @patch('kiwi.system_size.Command.run')
    def test_accumulate_files(self, mock_command):
        self.size.accumulate_files()
        mock_command.assert_called_once_with(
            ['bash', '-c', 'find source_dir | wc -l']
        )
