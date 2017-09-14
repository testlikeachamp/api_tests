import pytest


@pytest.fixture(scope="session",
                params=(['http://localhost:8000/', '10.0.2.2'], ['http://httpbin.org/', '50.54.242.152']),
                ids=['dev', 'prod'])
def base_url(request):
    print("Create fixture {}".format(request.param))
    return request.param
