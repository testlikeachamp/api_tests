import filecmp
import os


from requests import get


def test_image_png(base_url):
    r = get(base_url + 'image', headers={'Accept': 'image/png'})
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0

    filename = 'pig_png.png'
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    data_file_path = os.path.join(current_directory, filename)
    assert r.content == open(data_file_path, 'rb').read()

    with open('downloaded.png', 'wb') as f:
        f.write(r.content)
    assert filecmp.cmp('downloaded.png', data_file_path, shallow=False)


def test_image_webp(base_url):
    r = get(base_url + 'image', headers={'Accept': 'image/webp'})
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0

    filename = 'wolf_webp'
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    data_file_path = os.path.join(current_directory, filename)
    assert r.content == open(data_file_path, 'rb').read()

    with open('downloaded', 'wb') as f:
        f.write(r.content)
    assert filecmp.cmp('downloaded', data_file_path, shallow=False)


def test_image_svg(base_url):
    r = get(base_url + 'image', headers={'Accept': 'image/svg+xml'})
    assert r.status_code == 200
    assert r.reason == 'OK'
    assert r.elapsed.total_seconds() < 1.0

    filename = 'svg_svg.svg'
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    data_file_path = os.path.join(current_directory, filename)
    assert r.content == open(data_file_path, 'rb').read()

    with open('downloaded.svg', 'wb') as f:
        f.write(r.content)
    assert filecmp.cmp('downloaded.svg', data_file_path, shallow=True)
