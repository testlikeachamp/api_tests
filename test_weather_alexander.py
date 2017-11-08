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

# 354000 - Sochi
# 344000 - Rostov-on-Don
@pytest.mark.parametrize('zip_city, code_country, temp_max, temp_min, tem_average', [
    ('354000', 'RU', 29.1, -5.4, 8.1),
    ('344000', 'RU', 25.1, -25, 2.9),
])
def test_weather_zip_code(zip_city, code_country, temp_max, temp_min, tem_average):
    url = 'http://api.openweathermap.org/data/2.5/weather?zip='+zip_city+','+code_country+'&units=metric&appid='
    key = 'f1f0eead8298a901e9069ab5b02dcfdd'  # put your own key here :P
    r = get(url+key)
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')

    data = r.json()

    # Maxim/minimum temperature in celcius for November from Wikipedia
    # max 22.7
    # min -20.9
    # average 5,3 +- 5
    # check max/min
    assert temp_min < data['main']['temp'] < temp_max
    print('The temperature is now: ', data['main']['temp'])
    # check average temp
    assert tem_average-5 < data['main']['temp'] < tem_average+5
