import requests
from requests import get


# One way is to use config fixture directly
def test_ip(config):
    r = get(config['base_url']+'ip')
    assert r.status_code == 200
    assert r.json()['origin'] == config['my_ip']


# The other way is to use fixtures derived from from the config fixtures
def test_anything(base_url, my_ip):
    r = get(base_url + 'anything')
    assert r.status_code == 200
    assert r.json()['origin'] == my_ip
    assert r.json()['method'] == 'GET'


def test_uuid(base_url):
    r = get(base_url + 'uuid')
    assert r.status_code == 200
    assert list(r.json().keys()) == ['uuid']
    assert len(r.json()['uuid']) == 36


def test_user_agent(base_url):
    r = get(base_url + 'user-agent')
    assert r.status_code == 200
    assert r.json()['user-agent'] == 'python-requests/' + requests.__version__
