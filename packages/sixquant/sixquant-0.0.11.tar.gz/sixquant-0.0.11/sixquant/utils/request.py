# coding=utf-8

from io import StringIO

import pandas as pd

from .fetcher import fetcher
from .json import json2obj
from ..utils.datetime_utils import to_date_str, get_last_trading_day, get_prev_trade_day


def request_json_obj(url):
    """
    从网络中加载 JSON 数据返回 JSON 对象
    (支持压缩等，比原装的性能要好)
    :param url:
    :return: DataFrame
    """
    status, data = fetcher.http_get_json(url, charset='utf-8')
    if status == 200:
        return json2obj(data)
    return None


def request_json_dataframe(url):
    """
    从网络中加载 JSON 数据转换为 DataFrame 格式返回
    (支持压缩等，比原装的性能要好)
    :param url:
    :return: DataFrame
    """
    status, data = fetcher.http_get_json(url, charset='utf-8')
    if status == 200:
        if data is None or data == '' or data == 'null':
            return None
        return pd.DataFrame(pd.io.json.loads(data))
    return None


def request_dataframe(url, dtype=None):
    """
    从网络中加载 DataFrame，支持压缩等，比原装的性能要好
    :param url:
    :param dtype:
    :return: DataFrame
    """
    status, data = fetcher.http_get_text(url)
    if status == 200:
        return pd.read_csv(StringIO(data), dtype=dtype)
    return None


def request_dataframe_date(url, dt=None):
    if dt is not None:
        url += '/' + to_date_str(dt)
    return request_dataframe(url)


# =========================================================

def request_json_obj_date(url, dt=None, args=""):
    """
    请求获取多日数据
    :param url:
    :param dt:
    :return: JSON Object
    """
    if dt is not None:
        url += '/' + to_date_str(dt)
    url += args
    return request_json_obj(url)


def request_json_obj_days_date(url, dt=None, days=None, multiple=False):
    """
    请求获取多日数据
    :param url:
    :param days:
    :param dt:
    :param multiple: 是否进行多次请求获取多日数据
    :return: JSON Object
    """
    if multiple == False:
        if days is not None:
            url += '/' + str(days)
        if dt is not None:
            if days is None:
                url += '/1'
            url += '/' + to_date_str(dt)
        return request_json_obj(url)
    else:
        if days is None:
            if dt is not None:
                url += '/' + to_date_str(dt)
            return request_json_obj(url)
        else:
            if dt is None:
                dt = get_last_trading_day()

            dates = []
            for i in range(days):
                dates.append(to_date_str(dt))
                dt = get_prev_trade_day(dt)
            dates = sorted(dates)

            items = []
            for date in dates:
                data = request_json_obj(url + '/' + date)
                if data is not None:
                    items.append(data)
            return items


def request_json_dataframe_codes_date(url, codes=None, dt=None):
    """
    从网络中加载 JSON 数据返回 DataFrame
    (支持压缩等，比原装的性能要好)
    :param url:
    :param codes:
    :param dt:
     :return:
    """
    if codes is not None:
        url += '/' + codes
        if dt is not None:
            url += '/' + to_date_str(dt)
    elif dt is not None:
        url += '/-/' + to_date_str(dt)

    return request_json_dataframe(url)
