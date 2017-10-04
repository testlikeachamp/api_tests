import pytest
import requests
from requests import get
import sys




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


def test_deflated(config):
    r = get(config['base_url'] + 'deflate')

    assert r.json()['origin'] == config['my_ip']
    assert r.status_code == requests.codes.ok

    assert r.json()['headers']['Accept-Encoding'] == 'gzip, deflate'
    assert r.json()['headers']['User-Agent'] == 'python-requests/' + str(requests.__version__)
    assert r.elapsed.total_seconds() < 1.5
    assert r.reason == 'OK'
    assert r.json()['deflated'] == True


def test_brotli(config):
    r = get(config['base_url'] + 'brotli')
    assert r.status_code == requests.codes.ok
    assert r.elapsed.total_seconds() < 1.5
    assert r.reason == 'OK'
    assert len(r.content) > 0


@pytest.mark.parametrize('stat_cod', [
    200,
    300,
    400
])
def test_status(config, stat_cod):
    r = get(config['base_url'] + 'status/' + str(stat_cod))
    assert r.status_code == stat_cod
    assert r.elapsed.total_seconds() < 1.5


@pytest.mark.parametrize('key,val', [
    ('key-11', 'val-11'),
    ('key-22', 'val-22'),
])
def test_response_headers(config, key, val):
    r = get(config['base_url'] + 'response-headers?{0}={1}'.format(key, val))
    assert r.status_code == 200
    assert r.elapsed.total_seconds() < 1.5
    assert r.headers.get(key) == val


@pytest.mark.parametrize('page, cod_stat', [
    (':n', 404),
    (1, 302),
    (2, 302),
])
def test_redirect(config, page, cod_stat):
    r = get(config['base_url'] + 'redirect/' + str(page))
    # assert r.headers['location'] == '/get'
    assert r.status_code == cod_stat
    # assert r.elapsed.total_seconds() < 1.5





