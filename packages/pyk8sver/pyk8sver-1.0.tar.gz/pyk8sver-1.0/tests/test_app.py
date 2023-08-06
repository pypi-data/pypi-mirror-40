# -*- coding: utf-8 -*-
from mock import patch, MagicMock
from pytest import raises
import pytest
#from pyk8sver.app import A 
                          
@pytest.fixture
def useragent():
    return {'User-Agent': 'FakeSpider/1.0'}

def test_asset_class():
    assert 1 == 1
