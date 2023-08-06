# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import json
import requests


def url_get_host(url):
    """
    从URL中找出 HOST 部分
    get_host('http[s]://host[:port]/path') --> 'host'.
    :param url:
    :return:
    """
    if url is None or url == '':
        return None

    pos = url.find('://')
    if -1 != pos:
        url = url[pos + 3:]

    pos1 = url.find(':')
    if -1 == pos1:
        pos1 = len(url)

    pos2 = url.find('/')
    if -1 == pos2:
        pos2 = len(url)

    if pos2 < pos1:
        pos1 = pos2

    host = url[: pos1]
    return host


def http_get(target, charset=None):
    """
    Get
    :param target:
    :param charset:
    :return:
    """
    headers = {
        'Host': url_get_host(target),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Content-type': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    r = requests.get(target, headers=headers, timeout=60)

    if r.status_code != 200:
        return r.status_code, r.text

    if charset is not None:
        r.encoding = charset

    return r.status_code, r.text


def http_post_json(target, json_body, charset=None):
    """
    POST json
    :param target:
    :param json_body:
    :param charset:
    :return:
    """
    headers = {
        'Host': url_get_host(target),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Content-type': 'application/json;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    r = requests.post(target, json=json_body, headers=headers, timeout=60)

    if r.status_code != 200:
        return r.status_code, r.text

    if charset is not None:
        r.encoding = charset

    return r.status_code, r.text


session_server_address = None  # 登录服务器地址
session_token = None  # 登录Token


def login(address, crypted_username_password):
    """
    登录
    :param crypted_username_password:
    :param address:
    :return:
    """
    if address[-1] == '/':
        address = address[0:-1]

    target = address + '/api/v1/auth/login'
    post_json = {"cuserpwd": crypted_username_password}
    status_code, body = http_post_json(target, post_json)
    if status_code != 200:
        return False

    rs = json.loads(body)
    if rs['code'] != 20000:
        return False

    global session_server_address
    global session_token

    session_server_address = address
    session_token = rs['data']['token']
    return True


def http_get_json(target, charset=None):
    """
    下载JSON数据
    :param target:
    :param charset:
    :return:
    """
    global session_token
    target = session_server_address + target
    headers = {
        'Host': url_get_host(target),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Content-type': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Accept-Language': 'en-US,en;q=0.5',
        'Authorization': 'Bearer ' + session_token
    }
    r = requests.get(target, headers=headers, timeout=60)

    if r.status_code != 200:
        return False, None

    r.encoding = charset
    rs = json.loads(r.text)
    if rs['code'] != 20000:
        return False, None

    return True, rs['data']
