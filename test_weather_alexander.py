import time

import pytest
import requests
import json
from requests import get
import jsonschema
from jsonschema import validate


# TODO: test other endpoints
# TODO: add parametrization by the city


@pytest.mark.parametrize('name_city, name_country, ', [
    ('London', 'GB'),
    ('Moscow', 'RU'),
    ('Taganrog', 'RU'),
])
def test_weather(name_city, name_country):
    url = 'http://api.openweathermap.org/data/2.5/weather?q='+name_city+','+name_country+'&appid='
    key = 'f1f0eead8298a901e9069ab5b02dcfdd'  # put your own key here :P
    r = get(url+key)
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')

    data = r.json()
    example = {'base': 'stations',
               'clouds': {'all': 90},
               'cod': 200,
               'coord': {'lat': 51.51, 'lon': -0.13},
               'dt': 1485789600,
               'id': 2643743,
               'main': {'humidity': 81,
                        'pressure': 1012,
                        'temp': 280.32,
                        'temp_max': 281.15,
                        'temp_min': 279.15},
               'name': 'London',
               'sys': {'country': 'GB',
                       'id': 5091,
                       'message': 0.0103,
                       'sunrise': 1485762037,
                       'sunset': 1485794875,
                       'type': 1},
               'visibility': 10000,
               'weather': [{'description': 'light intensity drizzle',
                            'icon': '09d',
                            'id': 300,
                            'main': 'Drizzle'}],
               'wind': {'deg': 80, 'speed': 4.1}}

    assert data['name'] == name_city
    assert data['sys']['country'] == name_country
    assert data['main']['temp'] > 0

    try:
        jsonschema.validate(example, data)
    except jsonschema.ValidationError as e:
        print('Validation Error: ', e.message)
    except jsonschema.SchemaError as e:
        print('Schema Error: ', e.message)


# 'city_name': 'Sochi',
# 'code_country': 'RU',




year_temp = {
    '354000': {
        1: (1, 2),
            # {
            # 'temp_max': 1,
            # 'temp_min': 2},
        2: {
            'temp_max': 1,
            'temp_min': 2},
        3: {
            'temp_max': 1,
            'temp_min': 2},
        4: {
            'temp_max': 1,
            'temp_min': 2},
        5: {
            'temp_max': 1,
            'temp_min': 2},
        6 : {'temp_max': 1,
              'temp_min': 2},
        7: {'temp_max': 1,
              'temp_min': 2},
        8: {'temp_max': 1,
              'temp_min': 2},
        'SEP': {'temp_max': 1,
              'temp_min': 2},
        'OCT': {'temp_max': 1,
              'temp_min': 2},
        11: {
            'temp_max': 29.1,
            'temp_min': -5.4},
        12: {'temp_max': 1,
              'temp_min': 2},
    },
    '344000': {
        11: {
            'temp_max': 25.0,
            'temp_min': -25.1},
    }
}



# 354000 - Sochi
# 344000 - Rostov-on-Don
@pytest.mark.parametrize('zip_city, code_country', [
    ('354000', 'RU'),
    ('344000', 'RU')
])
def test_weather_zip_code(zip_city, code_country):
    url = 'http://api.openweathermap.org/data/2.5/weather?zip='+zip_city+','+code_country+'&units=metric&appid='
    key = 'f1f0eead8298a901e9069ab5b02dcfdd'  # put your own key here :P
    r = get(url+key)
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')

    data = r.json()
    # current month:
    month = time.gmtime().tm_mon
    print(zip_city, month)
    temp_min = year_temp[zip_city][month]['temp_min']
    temp_max = year_temp[zip_city][month]['temp_max']

    # create a table with temperatures for year around

    # Maximum/minimum temperature in celsius for November from Wikipedia
    # max 22.7
    # min -20.9
    # average 5,3 +- 5
    # check max/min
    assert temp_min < data['main']['temp'] < temp_max
    print('The temperature is now: ', data['main']['temp'])

    # check average temp
    # only valid when we gather data hourly every day for the whole month
    # assert tem_average-5 < data['main']['temp'] < tem_average+5
