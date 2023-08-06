# -*- coding: utf-8 -*-
from pytest import raises

import pytest
import logging
parametrize = pytest.mark.parametrize

from pyk8sver import metadata
from pyk8sver.main import main

class TestMain(object):
    @parametrize('helparg', ['-h', '--help'])
    def test_help(self, helparg, capsys):
        with raises(SystemExit) as exc_info:
            main(['progname', helparg])
        out, err = capsys.readouterr()
        assert 'usage' in out
        assert 'progname' in out
        assert exc_info.value.code == 0

    @parametrize('versionarg', ['-V', '--version'])
    def test_version(self, versionarg, capsys):
        with raises(SystemExit) as exc_info:
            main(['progname', versionarg])
        out, err = capsys.readouterr()
        assert out == '{0} {1}\n'.format(metadata.project, metadata.version)
        assert exc_info.value.code == 0
