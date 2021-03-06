import pytest
import requests
from requests import get, post


def test_httpbin_post(config):
    mydata = [{'name': 'Nikolay'}, 'hello']
    r = post(config['base_url'] + 'post', json=mydata)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['json'] == mydata
    assert r.elapsed.total_seconds() < 1.500


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


@pytest.mark.parametrize('connection', ['close', 'keep-alive'])
def test_gzip(base_url, connection, request):
    r = get(base_url + 'gzip', headers={'Connection': connection})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['gzipped'] == True
    assert data['headers']['User-Agent'] == 'python-requests/' + str(requests.__version__)
    if 'prod' in request.node.name:
        connection = 'close'  # prod server doesn't support keep-alive
    assert data['headers']['Connection'] == connection
    assert r.elapsed.total_seconds() < 0.500
