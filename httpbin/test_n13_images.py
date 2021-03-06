import filecmp
import os
import pytest


from requests import get


@pytest.mark.parametrize('test_format,test_image', [
    ('webp', 'wolf.webp'),
    ('png', 'pig.png'),
    ('svg+xml', 'svg_logo.svg')
])
def test_image_endpoint(base_url, test_format, test_image):
    r = get(base_url + 'image', headers={'Accept': 'image/'+test_format})
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0

    filename = test_image
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    data_file_path = os.path.join(current_directory, "images", filename)
    assert r.content == open(data_file_path, 'rb').read()

    tempfile = 'download.' + test_format
    with open(tempfile, 'wb') as f:
        f.write(r.content)
    assert filecmp.cmp(tempfile, data_file_path, shallow=False)
