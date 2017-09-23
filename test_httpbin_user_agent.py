
from requests import get
import requests

from conftest import config

def test_httpbin_user_agent(config):
    r = get(config['base_url'] + 'user-agent')
    assert r.status_code == 200, r.text
    assert r.reason == "OK", r.text
    assert r.json()['user-agent'] == 'python-requests/' + requests.__version__
    print(r.elapsed.total_seconds())
    #data = r.json()
    #assert len(r.json())
    #print(data)
    #print(r.reason)
