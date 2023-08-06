#!/usr/bin/env python3

from urllib import request
import json
import os
from ..utils import *

url_list = []

# test url: https://wenku.baidu.com/view/6f4ca758312b3169a451a4a7.html

def get_txt(page_url, path_file):
    # print('page_url: %s' % page_url)
    resp = request.urlopen(page_url)
    assert resp, resp.getcode() == 200

    page_data = resp.read()
    assert page_data

    page_data = page_data.decode('utf-8')
    assert page_data
    # print('page_data: %s' % page_data)

    page_json = json.loads(page_data.split('(', 1)[1].strip(')'))
    assert page_json
    # print(page_json)

    page_json = page_json['body']

    for i in page_json:
        if i['t'] == 'word':
            txt = i['c']

            if i['ps'] != None and '_enter' in i['ps'].keys():
                txt = '\n'

            # print(txt, end = '')

            with open(path_file, 'a') as f:
                f.write(txt)

def get_txt_wrapper(urls, path_file):
    urls = urls.replace('\\x22', '')
    assert urls

    urls = urls.replace('\\', '')
    assert urls

    urls = re.findall(r'pageLoadUrl:.*\w', urls)[0].split(',')
    # print('urls: %s' % urls)
    # print('urls length: %s' % len(urls))

    for url in urls:
        if 'json' in url:
            url_list.append(url.split(':', 1)[1].replace('}', '').strip(']'))

    # print("url_list length: %s" % len(url_list))

    for page_url in url_list:
        get_txt(page_url, path_file)

def wenku_baidu_download(url, output_dir = '.'):
    resp = request.urlopen(url)
    assert resp, resp.getcode() == 200
    print('resp.getcode: %s' % resp.getcode())

    data = resp.read()
    assert data

    data = data.decode('gb2312')
    assert data

    doc_title = r1(r'\'title\'\:\s+\'(.+)\'', data)
    assert doc_title
    print('doc_title: %s' % doc_title)

    doc_id = r1(r'\'docId\'\:\s+\'(.+)\'', data)
    assert doc_id
    print('doc_id: %s' % doc_id)

    doc_type = r1(r'\'docType\'\:\s+\'(.+)\'', data)
    assert doc_type
    print('doc_type: %s' % doc_type)

    wkinfo_htmlurls = r1(r'WkInfo.htmlUrls\s+\=\s+\'(.+)\'\;', data)
    assert wkinfo_htmlurls
    # print(wkinfo_htmlurls)

    output_dir = os.path.realpath(output_dir)
    path_file = doc_title + '.txt'
    path_file = os.path.join(output_dir, path_file)
    # print(path_file)

    if doc_type == 'doc':
        get_txt_wrapper(wkinfo_htmlurls, path_file)

    if os.path.exists(path_file) and os.path.getsize(path_file) > 0:
        print('Download OK: %s' % path_file)
    else:
        print('Download Nothing')

download = wenku_baidu_download
