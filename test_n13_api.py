import requests


def test_httpbin_post(config):
    mydata = [{'name': 'Nikolay'}, 'hello']
    r = requests.post(config['base_url'] + 'post', json=mydata)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['json'] == mydata
    assert r.elapsed.total_seconds() < 0.500


def test_httpbin_ip(config):
    r = requests.get(config['base_url'] + 'ip')
    assert r.status_code == 200, r.text
    data = r.json()
    assert data == {u'origin': config['my_ip']}
    assert r.elapsed.total_seconds() < 0.500


def test_user_agent(config):
    r = requests.get(config['base_url'] + 'user-agent')
    assert r.status_code == 200, r.text
    data = r.json()
    assert data == {u'user-agent': 'python-requests/' + str(requests.__version__)}
    assert r.elapsed.total_seconds() < 0.500
