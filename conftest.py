import pytest
from requests import get


class Config:
    def __init__(self, base_url, my_ip):
        self.base_url = base_url
        self.ip = my_ip


# Options to get router ip:
# ['https://api.ipify.org', 'http://bot.whatismyipaddress.com', 'http://ipv4bot.whatismyipaddress.com']
@pytest.fixture(scope='session',
                params=[
                    Config('http://localhost:8000/', '10.0.2.2'),
                    Config('http://localhost:8000/', '127.0.0.1'),
                    Config('http://httpbin.org/', get('http://bot.whatismyipaddress.com/').text)
                ],
                ids=['virt', 'dev', 'prod'])
def config(request):
    return request.param
