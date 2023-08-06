from intelex import get_version, echo

def test_get_version():
    assert get_version() == '0.0.17'

def test_echo():
    assert echo('Test') == 'Test'