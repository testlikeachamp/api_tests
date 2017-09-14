from requests import get


def test_ip(base_url):
    r = get(base_url[0]+'ip')
    assert r.status_code == 200
    assert r.json()['origin'] == base_url[1]


def test_anything(base_url):
    r = get(base_url[0] + 'anything')
    assert r.status_code == 200
    assert r.json()['origin'] == base_url[1]
    assert r.json()['method'] == 'GET'


