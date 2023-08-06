#!/usr/bin/env python3

from urllib import request
import json
import os
import gzip
from ..utils import *

# test url: https://wenku.baidu.com/view/6f4ca758312b3169a451a4a7.html

def get_doc(page_url, path_file):
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
            doc = i['c']

            if i['ps'] != None and '_enter' in i['ps'].keys():
                doc = '\n'

            # print(doc, end = '')

            with open(path_file, 'a') as f:
                f.write(doc)

def get_doc_wrapper(urls, path_file):
    urls = urls.replace('\\x22', '')
    assert urls

    urls = urls.replace('\\', '')
    assert urls

    urls = re.findall(r'pageLoadUrl:.*\w', urls)[0].split(',')
    # print('urls: %s' % urls)
    # print('urls length: %s' % len(urls))

    url_list = []

    for url in urls:
        if 'json' in url:
            url_list.append(url.split(':', 1)[1].replace('}', '').strip(']'))

    # print("url_list length: %s" % len(url_list))

    for page_url in url_list:
        get_doc(page_url, path_file)

def get_txt(url, path_file):
    resp = request.urlopen(url)
    assert resp, resp.getcode() == 200

    data = resp.read()
    assert data

    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1:
    # invalid start byte
    data = gzip.decompress(data).decode('utf-8')
    assert data
    # print(data)

    txt_json = json.loads(data.split('(', 1)[1].strip(')'))
    assert txt_json
    # print(txt_json)

    for page in txt_json:
        txt = page['parags'][0]['c']
        # print(txt)

        with open(path_file, 'a') as f:
            f.write(txt)

def get_txt_wrapper(url, path_file):
    resp = request.urlopen(url)
    assert resp, resp.getcode() == 200

    data = resp.read()
    assert data

    data = data.decode('utf-8')
    assert data

    json_data = json.loads(data.split('(', 1)[1].strip(')'))
    assert json_data
    # print('json_data: %s' % json_data)

    doc_id = json_data['doc_id']
    # print('doc_id: %s' % doc_id)

    md5sum = json_data['md5sum']
    # print('md5sum: %s' % md5sum)

    json_doc_info = json_data['docInfo']
    assert json_doc_info

    total_page_num = json_doc_info['totalPageNum']
    print('totalPageNum: %s' % total_page_num)

    rsign = json_data['rsign']
    # print('rsign: %s' % rsign)

    txt_json_url = 'https://wkretype.bdimg.com/retype/text/'
    txt_json_url += doc_id
    txt_json_url += '?'
    txt_json_url += md5sum
    txt_json_url += '&callback=cb&pn=1&rn='
    txt_json_url += total_page_num
    txt_json_url += '&rsign='
    txt_json_url += rsign

    get_txt(txt_json_url, path_file)

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

    output_dir = os.path.realpath(output_dir)
    path_file = doc_title + '.txt'
    path_file = os.path.join(output_dir, path_file)
    # print(path_file)

    if doc_type == 'doc':
        wkinfo_htmlurls = r1(r'WkInfo.htmlUrls\s+\=\s+\'(.+)\'\;', data)
        assert wkinfo_htmlurls
        # print(wkinfo_htmlurls)

        get_doc_wrapper(wkinfo_htmlurls, path_file)
    elif doc_type == 'txt':
        getdocinfo_url = 'https://wenku.baidu.com/api/doc/getdocinfo'
        getdocinfo_url = getdocinfo_url + '?callback=cb&doc_id=' + doc_id
        get_txt_wrapper(getdocinfo_url, path_file)
    else:
        print('Neither doc nor txt')

    if os.path.exists(path_file) and os.path.getsize(path_file) > 0:
        print('Download OK: %s' % path_file)
    else:
        print('Download Nothing')

download = wenku_baidu_download
