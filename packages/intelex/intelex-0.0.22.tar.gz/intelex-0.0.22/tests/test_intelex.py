from intelex import get_version, get_endpoint, get_apikey
import os

def test_get_version():
    assert get_version() == '0.0.22'

def test_get_endpoint():
    assert get_endpoint() == os.environ['ilx_endpoint']

def test_get_aoikey():
    assert get_apikey() == os.environ['ilx_apikey']