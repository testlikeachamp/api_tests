from requests import get

import jsonschema
import pytest
import time


# TODO: test other endpoints
# TODO: add parametrization by the city

@pytest.mark.parametrize('city_name, country_code', [
    ('Milan', 'IT'),
    ('Manchester', 'GB'),
    ('Naples', 'IT'),
])
def test_weather(city_name, country_code):
    key = '54044d3988d832f0d568ebbb12a2cd58'  # put your own key here :P
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name+','+country_code,
        'appid': key,
        'units': 'metric',
    }
    r = get(url, params=params)
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 2.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')

    data = r.json()
    example = {'base': 'stations',
               'clouds': {'all': 0},
               'cod': 200,
               'coord': {'lat': 45.46, 'lon': 9.19},
               'dt': 1512343200,
               'id': 6542283,
               'main': {'humidity': 83,
                        'pressure': 1025,
                        'temp': -0.54,
                        'temp_max': 1,
                        'temp_min': -2},
               'name': 'Milan',
               'sys': {'country': 'IT',
                       'id': 5800,
                       'message': 0.0025,
                       'sunrise': 1512283570,
                       'sunset': 1512315637,
                       'type': 1},
               'visibility': 10000,
               'weather': [{'description': 'clear sky',
                            'icon': '01n',
                            'id': 800,
                            'main': 'Clear'}],
               'wind': {'deg': 20.5004, 'speed': 3.01}}
    assert data['name'] == city_name
    assert data['sys']['country'] == country_code

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

year_temp_ranges = {
    '80121': {
        1: (-5, 21.1),
        2: (-5, 22.5),
        3: (-3, 28.0),
        4: (-1, 30.5),
        5: (1,   34.1),
        6: (7.8,   37),
        7: (11.7,  39),
        8: (10,  40),
        9: (6.8, 37.2),
        10: (3, 31.5),
        11: (-2, 29.4),
        12: (-4.5, 24.4)
    },
    '20121': {
        1: (-17.3, 23.1),
        2: (-17.8, 24.8),
        3: (-11.1, 28.3),
        4: (-4.9, 31.9),
        5: (1.2,  35),
        6: (1.2,  37.2),
        7: (7.5,   38.3),
        8: (7.8,   38.2),
        9: (-0.7, 35.1),
        10: (-2.9, 30),
        11: (-9.1, 22.4),
        12: (-14.3, 18.9)
    }
}


# 80121 - Napoli
# 20121 - Milan
@pytest.mark.parametrize('zip_code, country_cod', [
    ('80121', 'IT'),
    ('20121', 'IT')
])
def test_weather_zip_code(zip_code, country_cod):
    url = 'http://api.openweathermap.org/data/2.5/weather'

    key = '54044d3988d832f0d568ebbb12a2cd58'  # put your own key here :P
    params = {'zip': zip_code+','+country_cod,
              'units': 'metric',
              'appid': key}
    r = get(url, params=params)
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 2.0
    assert r.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert r.headers['Content-Type'].startswith('application/json')

    data = r.json()
    # current month:
    month = time.gmtime().tm_mon

    temp_min, temp_max = year_temp_ranges[zip_code][month]

    assert temp_min < data['main']['temp'] < temp_max
    print('The temperature is now: ', data['main']['temp'])
