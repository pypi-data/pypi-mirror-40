# coding=utf-8

import datetime
from functools import lru_cache

import pandas as pd

from ..constants import INDEXS, INDEX_NAMES, NAMES_URL, BASICS_URL, THRESHOLD_SMALL_CAP
from ..utils.daily_func_cache_watcher import daily_func_cache_watcher
from ..utils.datetime_utils import add_months
from ..utils.request import request_json_obj_date

"""
股票基本信息
"""


def get_names(dt=None):
    """
    得到股票名称列表
    :return:
        DataFrame
                        代码
        name            股票名称
    """
    # df = daily_cache.get('names')
    # if df is None:
    rs = request_json_obj_date(NAMES_URL, dt)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['code', 'name'])
    df.set_index('code', inplace=True)
    df.index.name = None

    # daily_cache.set('names', df)

    # return df.copy()  # 缓存的数据复制一份，以防止外面修改
    return df


def get_basics(dt=None, fields=['name', 'circulate',
                                'pe', 'pb', 'pledge',
                                'style', 'categories',
                                'margin', 'state', 'reason']):
    """
    得到股票基本信息列表
    :return:
        DataFrame
                        代码
        name            股票名称
        launch_date     上市日期
        pe              市盈率
        circulation     流通股本（亿股）
        capital         流通市值（亿元）
    """
    # df = daily_cache.get('basics')
    # df = None
    # if df is None:
    rs = request_json_obj_date(BASICS_URL, dt)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['code', 'name', 'circulate', 'pe', 'pb', 'pledge',
                                   'style', 'categories',
                                   'margin', 'state', 'reason'])
    df.set_index('code', inplace=True)
    df.index.name = None

    # daily_cache.set('basics', df)
    # return df.copy()  # 缓存的数据复制一份，以防止外面修改
    return df


@lru_cache(None)
def get_stock_name(stock):
    """
    得到股票名称
    :param stock:
    :return:
    """
    daily_func_cache_watcher.watch_lru_cache(get_stock_name)

    df = get_basics()
    rs = df.loc[stock]['name']

    return rs


@lru_cache(None)
def get_stock_pe(stock):
    """
    得到股票PE
    :param stock:
    :return:
    """
    daily_func_cache_watcher.watch_lru_cache(get_stock_pe)

    df = get_basics()
    rs = df.loc[stock]['pe']

    return rs


@lru_cache(None)
def get_stock_circulation(stock):
    """
    得到股票流通盘（亿股）
    :param stock:
    :return:
    """
    daily_func_cache_watcher.watch_lru_cache(get_stock_circulation)

    df = get_basics()
    rs = df.loc[stock]['circulation']

    return rs


@lru_cache(None)
def get_stock_capital(stock):
    """
    得到股票流通市值（亿元）
    :param stock:
    :return:
    """
    daily_func_cache_watcher.watch_lru_cache(get_stock_capital)

    df = get_basics()
    rs = df.loc[stock]['capital']

    return rs


def get_stocks(small_only=False, st_only=False, subnew_only=False, no_st=False, no_subnew=False):
    """
    返回股票列表
    :param small_only: 是否只要小市值股
    :param st_only: 是否只要 ST 股
    :param subnew_only: 是否只要次新股（一年以内的股票称为次新股）
    :param no_st: 是否包含 ST 股
    :param no_subnew: 是否包含次新股（一年以内的股票称为次新股）
    :return:
    """
    df = get_basics()
    if df is None or len(df) == 0:
        return []

    if small_only:
        df = df[df.capital <= THRESHOLD_SMALL_CAP / 10000 / 10000]

    if st_only:
        df = df[df['name'].str.contains(r'^\*ST*')]  # *ST 开头的股票

    if subnew_only:
        df = df[df.launch_date >= add_months(datetime.date.today(), -12)]

    if no_st:
        df = df[~df['name'].str.contains(r'^\*ST*')]  # *ST 开头的股票

    if no_subnew:
        df = df[df.launch_date < add_months(datetime.date.today(), -12)]

    rs = df.index.values

    return rs


def get_launch_date(stocks):
    """
    得到股票上市日期
    :param stocks:
    :return:
    """
    df = get_basics()
    df = df['launch_date']

    if isinstance(stocks, str):
        rs = df.loc[stocks] if len(df) > 0 else None
    else:
        rs = df.loc[stocks]

    return rs


@lru_cache(None)
def _translate_stock_code(code):
    """
    得到股票内部代码
    名称转代码,例如 '上证50'->''
    :param code:
    :return:
    """
    try:
        i = INDEX_NAMES.index(code)
        return INDEXS[i]
    except ValueError:
        return code


def translate_stock_code(code_or_codes):
    """
    得到股票内部代码
    名称转代码,例如 '上证50'->''
    :param code_or_codes:
    :return:
    """
    if code_or_codes is None:
        return None

    if not isinstance(code_or_codes, str):
        rs = []
        for code in code_or_codes:
            rs.append(_translate_stock_code(code))

        return rs

    return _translate_stock_code(code_or_codes)
