import time

import pytest
import requests
import json
from requests import get
import jsonschema
from jsonschema import validate
import os


# TODO: test other endpoints
# TODO: add parametrization by the city

@pytest.mark.parametrize('city_name, country_code', [
    ('Manchester', 'GB'),
    ('Milan', 'IT'),
    ('Krasnodar', 'RU'),
])
def test_weather(city_name, country_code):
    key = '54044d3988d832f0d568ebbb12a2cd58'  # put your own key here :P
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name+','+country_code,
        'appid': key}
    r = get(url, params=params)
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')
