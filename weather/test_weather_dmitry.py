import time

import jsonschema
import pytest
from requests import get, delete, post, put, patch, head, options


# TODO: test other endpoints
# TODO: add parametrization by the city


@pytest.mark.parametrize('city_name, country_code', [
    ('London', 'GB'),
    ('Moscow', 'RU'),
    ('Taganrog', 'RU'),
])
def test_weather(city_name, country_code):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    key = 'f1f0eead8298a901e9069ab5b02dcfdd'  # put your own key here :P
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

    assert data['name'] == city_name
    assert data['sys']['country'] == country_code
    assert data['main']['temp'] > 0

    # http://json.org/
    # http://json-schema.org/examples.html
    # http://json-schema.org/example1.html
    # https://stackoverflow.com/questions/30868023/json-schema-require-all-properties

    # from jsonschema import validators
    # print(validators.Draft4Validator.DEFAULT_TYPES)

    _array_ = 'array'
    _boolean_ = 'boolean'
    _integer_ = 'integer'
    _null_ = 'null'
    _number_ = 'number'
    _object_ = 'object'
    _string_ = 'string'
    _type_ = 'type'
    _properties_ = 'properties'
    _required_ = 'required'
    _additional_properties_ = 'additionalProperties'

    schema = {
        _type_: _object_,
        _properties_: {
            'base': {_type_: _string_},
            'clouds': {
                _type_: _object_,
                _properties_: {
                    'all': {_type_: _integer_}}},
            'cod': {_type_: _integer_},
            'coord': {_type_: _object_},
            'dt': {_type_: _integer_},
            'id': {_type_: _integer_},
            'main': {_type_: _object_},
            'name': {_type_: _string_},
            'sys': {_type_: _object_},
            'visibility': {_type_: _integer_},
            'weather': {_type_: _array_},
            'wind': {_type_: _object_},
        },
        _required_: list(example.keys()),
        _additional_properties_: False
    }

    jsonschema.validate(data, schema)


#################################################################################
# a table with year around maximum/minimum temperatures in celsius from Wikipedia
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
@pytest.mark.parametrize('zip_code, country_code', [
    ('354000', 'RU'),
    ('344000', 'RU')
])
def test_weather_zip_code(zip_code, country_code):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    key = 'f1f0eead8298a901e9069ab5b0badkey'  # put your own key here :P
    params = {'zip': zip_code+','+country_code,
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
    # check average temp
    # only valid when we gather data hourly every day for the whole month
    # assert tem_average-5 < data['main']['temp'] < tem_average+5


# 0 ... 600 MB/min 0 0-1 -10 700MB 700000 MB


@pytest.mark.parametrize('city_name, country_code', [
    ('London', 'GB')
])
@pytest.mark.parametrize('method', [delete, put, patch, options])
def test_weather_delete(city_name, country_code, method):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    key = 'f1f0eead8298a901e9069ab5b02dcfdd'  # put your own key here :P
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name+','+country_code,
        'appid': key}
    r = method(url, params=params)
    assert r.status_code == 405
    assert r.reason == "Method Not Allowed"
    assert r.json() == {"cod": "405", "message": "Internal error"}


# TODO: test /weather endpoint with valid methods post and head
