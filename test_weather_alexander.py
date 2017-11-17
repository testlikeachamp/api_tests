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


@pytest.mark.parametrize('name_city, name_country, ', [
    ('London', 'GB'),
    ('Moscow', 'RU'),
    ('Taganrog', 'RU'),
])
def test_weather(name_city, name_country):
    url = 'http://api.openweathermap.org/data/2.5/weather?'
    key = 'f1f0eead8298a901e9069ab5b02dcfdd'  # put your own key here :P

    params = {'q': ','.join([name_city, name_country]),
              'units': 'metric',
              'appid': key}
    r = get(url, params=params)


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




year_temp_ranges = {
    '354000': {
        1: (-13,   21.5),
        2: (-12.6, 23.5),
        3: (-7,    30.0),
        4: (-3.8,  31.7),
        5: (3.0,   34.7),
        6: (7.1,   35.2),
        7: (12.6,  39.4),
        8: (10.4,  38.5),
        9: (2.7,   36.0),
        10: (-3.2, 32.1),
        11: (-5.4, 29.1),
        12: (-8.3, 23.5)
    },
    '344000': {
        1: (-31.9, 15.0),
        2: (-30.9, 19.8),
        3: (-28.1, 26.0),
        4: (-10.4, 33.6),
        5: (-4.3,  35.6),
        6: (-0.1,  38.4),
        7: (7.6,   39.6),
        8: (2.6,   40.1),
        9: (-4.6, 38.1),
        10: (-10.4, 31.0),
        11: (-25.1, 25.0),
        12: (-28.5, 18.5)
    }
}


# 354000 - Sochi
# 344000 - Rostov-on-Don
@pytest.mark.parametrize('zip_code, country_cod', [
    ('354000', 'RU'),
    ('344000', 'RU')
])
def test_weather_zip_code(zip_code, country_cod):
    url = 'http://api.openweathermap.org/data/2.5/weather'

    key = 'f1f0eead8298a901e9069ab5b02dcfdd'  # put your own key here :P
    params = {'zip': zip_code+','+country_cod,
              'units': 'metric',
              'appid': key}
    r = get(url, params=params)
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')

    data = r.json()
    # current month:
    month = time.gmtime().tm_mon

    temp_min, temp_max = year_temp_ranges[zip_code][month]

    assert temp_min < data['main']['temp'] < temp_max
    print('The temperature is now: ', data['main']['temp'])


@pytest.mark.parametrize('coord_lat, coord_lon, point_name', [
    ('43.6', '39.7303', 'Sochi'),
])
def test_weather_geo_coords(coord_lat, coord_lon, point_name):
    url = 'http://api.openweathermap.org/data/2.5/weather'

    key = 'f1f0eead8298a901e9069ab5b02dcfdd'  # put your own key here :P
    params = {'lat': coord_lat,
              'lon': coord_lon,
              'units': 'metric',
              'appid': key}

    r = get(url, params=params)
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')

    data = r.json()

    assert data['wind']['speed'] < 10
    assert data['name'] == point_name
    print('The temperature is now: ', data['wind']['speed'])
    print('City name is: ', data['name'])


@pytest.mark.parametrize('lon_left, lat_bottom, lon_right, lat_top, zoom , city_in_zone', [
    ('39', '43', '40', '44', '10', ['Adler', 'Lazarevskoye', 'Sochi']),
])
def test_weather_rect_zone(lon_left, lat_bottom, lon_right, lat_top, zoom, city_in_zone):
    url = 'http://api.openweathermap.org/data/2.5/box/city?'

    key = 'f1f0eead8298a901e9069ab5b02dcfdd'
    params = {'bbox': ','.join([lon_left, lat_bottom, lon_right, lat_top, zoom]),
              'appid': key}

    r = get(url, params=params)

    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')

    data = r.json()
    assert data['list'][0]['name'] == 'Lazarevskoye'

    city_list = []
    for i in range(len(data['list'])):
        city_list.append(str(data['list'][i]['name']))
    assert sorted(city_list) == city_in_zone


@pytest.mark.parametrize('city_id, city_name', [
    ('5809844,491422,484907', ['Seattle', 'Sochi', 'Taganrog']),
])
def test_weather_id(city_id, city_name):
    url = 'http://api.openweathermap.org/data/2.5/group?'

    key = 'f1f0eead8298a901e9069ab5b02dcfdd'
    params = {'id': city_id,
              'units': 'metric',
              'appid': key}

    r = get(url, params=params)

    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')

    data = r.json()

    city_list = []
    for i in range(len(data['list'])):
        city_list.append(str(data['list'][i]['name']))
    assert sorted(city_list) == city_name
