import pytest
from requests import get


# Options to get router ip:
# ['https://api.ipify.org', 'http://bot.whatismyipaddress.com', 'http://ipv4bot.whatismyipaddress.com']
@pytest.fixture(scope='session',
                params=[
                    {
                        'base_url': 'http://localhost:8000/',
                        'my_ip': '10.0.2.2'
                    },
                    {
                        'base_url': 'http://localhost:8000/',
                        'my_ip': '127.0.0.1'
                    },
                    {
                        'base_url': 'http://httpbin.org/',
                        'my_ip': get('http://bot.whatismyipaddress.com/').text
                    }
                ],
                ids=['virt', 'dev', 'prod'])
def config(request):
    return request.param


@pytest.fixture(scope='session')
def base_url(config):
    return config['base_url']


@pytest.fixture(scope='session')
def my_ip(config):
    return config['my_ip']
