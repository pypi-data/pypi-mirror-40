import re
from urllib import request

def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)

def get_url_file_ext_size(url):
    resp = request.urlopen(url)
    assert resp, resp.getcode() == 200

    type = resp.headers['Content-Type']
    type_dict = {
        'video/3gpp': '3gp',
        'video/f4v': 'flv',
        'video/mp4': 'mp4',
        'video/webm': 'webm',
        'video/x-flv': 'flv'
    }

    assert type in type_dict, type

    ext = type_dict[type]
    size = resp.headers['Content-Length']

    return ext, size
