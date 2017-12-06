import filecmp
import os

from requests import get


def test_image(config):
    r = get(config['base_url'] + 'image', headers={'Accept': 'image/jpeg'})
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0
    assert r.headers['Content-Type'] == 'image/jpeg'

    filename = 'wolf.jpg'
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    data_file_path = os.path.join(current_directory, "images", filename)
    assert r.content == open(data_file_path, 'rb').read()

    with open('downloaded.jpeg', 'wb') as f:
        f.write(r.content)
    assert filecmp.cmp('downloaded.jpeg', data_file_path, shallow=False)
