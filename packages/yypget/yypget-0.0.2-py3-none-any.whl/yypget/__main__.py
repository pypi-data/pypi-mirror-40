#!/usr/bin/env python

import sys, getopt
import argparse
from .utils import *
from .executor import *

def download_wrapper(url, output_dir = '.'):
    host = r1(r'https?://([^/]+)/', url)
    assert(host)

    if host.endswith('.com.cn'):
        host = host[:-3]

    """
    domain = r1(r'(\.[^.]+\.[^.]+)$', host)
    assert(domain)

    site = r1(r'([^.]+)', domain)
    assert(site)
    """

    site = r1(r'([a-zA-Z0-9]+\.[a-zA-Z0-9]+)', host)
    assert(site)
    print(site)

    supported_sites = {
        'sv.baidu': sv_baidu,
        'wenku.baidu': wenku_baidu,
    }

    if site in supported_sites:
        m = supported_sites[site]
    else:
        raise NotImplementedError(site)

    m.download(url, output_dir = output_dir)

def yypget_main(download):
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar = 'URL')
    parser.add_argument('-o', '--output-dir', help = 'set output directory')

    url = ''
    output_dir = '.'

    args = parser.parse_args()
    if args.url:
        url = args.url

    if args.output_dir:
        output_dir = args.output_dir

    download(url, output_dir)

def main(**kwargs):
    yypget_main(download_wrapper)

if __name__ == '__main__':
    main()
