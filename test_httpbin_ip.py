import pytest
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


@pytest.mark.parametrize('user,password', [
    ('user', 'password123'),
    ('_____', '83476235')])
def test_basic_auth(base_url, user, password):
    base_url = '//{0}:{1}@'.join(base_url.split('//')).format(user, password)
    r = get(base_url + 'basic-auth/{0}/{1}'.format(user, password))
    assert r.status_code == 200
    assert r.json() == {'authenticated': True, 'user': user}


@pytest.mark.parametrize('user,password', [
    ('user', 'password123'),
    ('_____', '83476235')])
def test_basic_auth_2(base_url, user, password):
    r = get(base_url + 'basic-auth/{0}/{1}'.format(user, password), auth=(user, password))
    assert r.status_code == 200
    assert r.json() == {'authenticated': True, 'user': user}


def test_deflated(base_url, my_ip):
    r = get(base_url + 'deflate')
    assert r.json()['method'] == 'GET'
    assert r.json()['origin'] == my_ip
    assert r.status_code == requests.codes.ok
    assert r.json()['headers']['Host'] == base_url[7:-1]
    assert r.json()['headers']['Accept'] == '*/*'
    assert r.json()['headers']['Accept-Encoding'] == 'gzip, deflate'
    if base_url == 'http://localhost:8000/':
        assert r.json()['headers']['Connection'] == 'keep-alive'
    elif base_url == 'http://httpbin.org/':
        assert r.json()['headers']['Connection'] == 'close'
    assert r.json()['headers']['User-Agent'] == 'python-requests/2.18.4'
    # here i have a problem with encoding
    # assert r.json()['headers'] == r.headers

    payload = {'key1': 'value1', 'key2': 'value2'}
    p = requests.get(base_url + 'deflate', params=payload)
    assert r.url + '?key1=value1&key2=value2' == p.url

    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.post(base_url + 'deflate', data=payload)
    assert r.status_code == 405







