import argparse
import os
import re

import requests
from bs4 import BeautifulSoup

from database import (create_table, get_urls_length, get_counter, get_url_by_id, insert_url, url_exists,
                      increment_counter)


# If this url has html content and does not responds 4* or 5* will return True else False
def is_good_url(_url, domain):
    try:
        # remove /
        domain = domain[:-1] if domain.startswith('/') else domain
        if not _url or 'http' not in _url or not _url.startswith(domain):
            return False
        _res = requests.head(_url, )
        if str(_res.status_code).startswith('4') or str(_res.status_code).startswith('5'):
            return False
        if 'html' in _res.headers['Content-Type']:
            return True
    except Exception as e:
        print(str(e))
        return False
    return False


# If url has media, returns True else False.
def is_media(_url, domain='', check_domain=True):
    try:
        # remove /
        domain = domain[:-1] if domain.startswith('/') else domain
        if check_domain and not _url or 'http' not in _url or not _url.startswith(domain):
            return False
        _res = requests.head(_url, )
        if str(_res.status_code).startswith('4') or str(_res.status_code).startswith('5'):
            return False
        if 'html' not in _res.headers['Content-Type']:
            return True
    except Exception as e:
        print(str(e))
        return False
    return False


# Remove url parameters
def pretty_url(_url):
    _url = re.sub(r'([#?]).*?($)', '/', _url)
    if _url.startswith('https://'):
        _url = (_url[:9], _url[9:])
    elif _url.startswith('http://'):
        _url = (_url[:8], _url[8:])
    else:
        _url = ('', _url)

    _url = _url[0] + re.sub(r'/+', '/', _url[1])
    _url = re.sub(r'/*$', '', _url)
    return _url


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Staring url',)
    args = parser.parse_args()

    # Starting point for crawling
    start_url = args.url
    create_table()
    insert_url(start_url)
    counter = get_counter()
    urls_length = get_urls_length()
    while urls_length >= counter:
        url = get_url_by_id(counter)
        print(f'len(urls) = {urls_length}, counter = {counter}')
        if is_good_url(url, start_url):
            res = requests.get(url, )

            if str(res.status_code).startswith('4') or str(res.status_code).startswith('5'):
                print(f'status code {url} is {res.status_code}. crawler failed.')

            soup = BeautifulSoup(res.text, 'html.parser')

            new_urls = [pretty_url(href['href']) for href in soup.find_all('a') if
                        href['href'] and pretty_url(href['href']) and '..' not in pretty_url(href['href'])]

            for new_url in new_urls:
                if not new_url.startswith('http://') and not new_url.startswith('https://'):
                    new_url = os.path.join(res.url, new_url)
                if not url_exists(new_url):
                    insert_url(new_url)
        elif is_media(url, start_url):
            output_file = open('links.txt', 'a')
            output_file.write(f'{url}\n')
            output_file.close()

        increment_counter()
        counter = get_counter()
        urls_length = get_urls_length()
