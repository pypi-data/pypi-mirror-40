#!/usr/bin/env python3

from urllib import request
import json
import os
import sys
import math
from ..utils import *

# test 1st url:
# https://tv.sohu.com/v/cGwvOTM1ODU4Mi85MDQxMjI4OS5zaHRtbA==.html

# test 2nd url:
# https://tv.sohu.com/v/MjAxODEyMjAvbjYwMDY0MDAwNy5zaHRtbA==.html

def get_tv_sohu_true_url(su):
    true_url_url = 'https://data.vod.itc.cn/ip?new='
    true_url_url += su
    # print(true_url_url)

    true_url_resp = request.urlopen(true_url_url)
    assert true_url_resp, true_url_resp.getcode() == 200

    true_url_data = true_url_resp.read().decode('utf-8')
    assert true_url_data
    # print(true_url_data)

    true_url_json = json.loads(true_url_data)
    assert true_url_json
    # print(true_url_json)

    true_url = true_url_json['servers'][0]['url']
    assert true_url
    # print(true_url)

    return true_url

def urlretrieve_callback(count, size, total):
    sys.stdout.write('\rDownloading: [%d/%d]' % (count, math.ceil(total / size)))
    sys.stdout.flush()

def tv_sohu_download(url, output_dir = '.'):
    resp = request.urlopen(url)
    assert resp, resp.getcode() == 200

    data = resp.read()
    assert data

    data = data.decode('GBK')
    assert data
    # print(data)

    info_resp = ''
    info_data = ''

    vid = r1(r',vid:\s+\'(.+)\'', data)

    if vid:
        print('vid: %s' % vid)
        query_info_url = 'https://my.tv.sohu.com/play/videonew.do?vid='
        query_info_url += vid
        print(query_info_url)

        info_resp = request.urlopen(query_info_url)
        assert info_resp, info_resp.getcode() == 200

        info_data = info_resp.read().decode('GBK')
        assert info_data
        # print(info_data)
    else:
        vid = r1(r'vid="(\d+)"', data)
        assert vid
        print('vid: %s' % vid)

        query_info_url = 'https://hot.vrs.sohu.com/vrs_flash.action?vid='
        query_info_url += vid
        print(query_info_url)

        info_resp = request.urlopen(query_info_url)
        assert info_resp, info_resp.getcode() == 200

        info_data = info_resp.read().decode('utf-8')
        assert info_data
        # print(info_data)

    info_json = json.loads(info_data)
    assert info_json
    # print(info_json)

    title = info_json['data']['tvName']
    print(title)

    output_dir = os.path.realpath(output_dir)
    video_file = os.path.join(output_dir, title)

    true_url = ''

    clip_count = len(info_json['data']['clipsBytes'])
    if clip_count == 1:
        print('Need to download 1 file')
        su = info_json['data']['su'][0]
        assert su

        true_url = get_tv_sohu_true_url(su)
        video_file += '.mp4'

        request.urlretrieve(true_url, video_file, urlretrieve_callback)

        if os.path.getsize(video_file) == info_json['data']['totalBytes']:
            print('\nDownload OK: \"%s\"' % video_file)
        else:
            print('\nDownload Nothing')
    else:
        print('Need to download %s files' % clip_count)

        total_download_bytes = 0

        for i in range(clip_count):
            su = info_json['data']['su'][i]
            assert su

            true_url = get_tv_sohu_true_url(su)
            video_clip_file = video_file + '%02d' % (i + 1) + '.mp4'

            request.urlretrieve(true_url, video_clip_file, urlretrieve_callback)
            print('\nDownload OK: \"%s\"' % video_clip_file)

            total_download_bytes += os.path.getsize(video_clip_file)

        total_clips_bytes = sum(map(int, info_json['data']['clipsBytes']))
        if total_clips_bytes == total_download_bytes:
            print('All files download OK')
        else:
            print('Not all files downloaded')

download = tv_sohu_download
