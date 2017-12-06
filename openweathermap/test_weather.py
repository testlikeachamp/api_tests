from requests import get

RESPONSE_TIME = 2.0


# TODO: test other endpoints
# TODO: add parametrization by the city
def test_weather():
    url = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid='
    key = 'f1f0eead8298a901e9069ab5b02dcfdd'  # put your own key here :P
    r = get(url+key)
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < RESPONSE_TIME
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
    keys = {'main', 'visibility', 'cod', 'coord', 'wind', 'clouds', 'sys', 'name', 'dt', 'weather', 'id', 'base'}
    assert set(data) == keys
    # TODO: assert nested dicts and lists
    assert data['name'] == 'London'
    assert data['sys']['country'] == 'GB'
    assert data['main']['temp'] > 0
