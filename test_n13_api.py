import pytest
import requests
from requests import get, post


def test_httpbin_post(config):
    mydata = [{'name': 'Nikolay'}, 'hello']
    r = post(config['base_url'] + 'post', json=mydata)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['json'] == mydata
    assert r.elapsed.total_seconds() < 0.500


def test_httpbin_ip(config):
    r = get(config['base_url'] + 'ip')
    assert r.status_code == 200, r.text
    data = r.json()
    assert data == {u'origin': config['my_ip']}
    assert r.elapsed.total_seconds() < 0.500


def test_user_agent(config):
    r = get(config['base_url'] + 'user-agent')
    assert r.status_code == 200, r.text
    data = r.json()
    assert data == {u'user-agent': 'python-requests/' + str(requests.__version__)}
    assert r.elapsed.total_seconds() < 0.500


def test_deflate(config):
    r = get(config['base_url'] + 'deflate')
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['deflated'] == True
    assert data['headers']['User-Agent'] == 'python-requests/' + str(requests.__version__)
    assert r.elapsed.total_seconds() < 0.500


@pytest.mark.parametrize('input_connection','expected_connection',[
    ('close', 'close'),
    ('keep-alive', 'keep-alive')])
def test_gzip(base_url, input_connection, expected_connection):
    r = get(base_url + 'gzip', headers={'Connection': input_connection})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['gzipped'] == True
    assert data['headers']['User-Agent'] == 'python-requests/' + str(requests.__version__)
    assert data['headers']['Connection'] == expected_connection
    assert r.elapsed.total_seconds() < 0.500
