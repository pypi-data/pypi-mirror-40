# -*- coding: UTF-8 -*-

from ..constants import MARKET_GUAUGE_URL, MARKET_COUNTDIST_URL, MARKET_COUNT_URL, \
    MARKET_MONEY_URL, MARKET_MONEY_HGT_URL, MARKET_MONEY_SGT_URL, \
    MARKET_RATE_URL, MARKET_ORDER_URL, \
    MARKET_CRAZY_COUNT_URL, CATEGORY_CRAZY_COUNT_URL
from ..utils.request import request_json_obj_days_date
import pandas as pd
import numpy as np


def request_json_dataframe_days_date(url, dt, days, dims, columns, index, dtype=float):
    rs = request_json_obj_days_date(url, dt, days)
    if rs is None:
        return None

    df = None
    if days is None:
        b = rs.list
        if dims == 1:
            b = [b]
        a = np.repeat(rs.date, len(b))
        data = np.c_[a, b]
        df = pd.DataFrame(data, columns=columns)
    else:
        data = None
        for d in rs:
            if dims == 1:
                b = np.array([d.list])
            else:
                b = np.array(d.list)
            a = np.repeat(d.date, len(b))
            if data is None:
                data = np.c_[a, b]
            else:
                data = np.r_[data, np.c_[a, b]]
        if data is None:
            return None
        df = pd.DataFrame(data, columns=columns)

    df.set_index(index, inplace=True)
    df = df.astype(dtype)
    return df


def get_market_gauge(dt=None, days=None):
    """
    大盘温度
    """
    return request_json_dataframe_days_date(MARKET_GUAUGE_URL,
                                            dt, days,
                                            dims=1,
                                            columns=['date', 'js', 'zj', 'zh'],
                                            index=['date'],
                                            dtype=float)


def get_market_countdist(dt=None, days=None):
    """
    涨跌分布
    """
    return request_json_dataframe_days_date(MARKET_COUNTDIST_URL,
                                            dt, days,
                                            dims=1,
                                            columns=['date', 'dt', 'd8', 'd86', 'd65', 'd54', 'd42', 'd20', 'z02',
                                                     'z24', 'z45', 'z56', 'z68', 'z8', 'zt'],
                                            index=['date'],
                                            dtype=int)


def get_market_crazy_count(dt=None, days=None):
    """
    市场情绪统计（竞价/涨停/炸板/跌停/自然涨停/跌停翘板数）
    """
    return request_json_dataframe_days_date(MARKET_CRAZY_COUNT_URL,
                                            dt, days,
                                            dims=1,
                                            columns=['date', 'jj', 'zt', 'zb', 'dt', 'zz', 'qb'],
                                            index=['date'],
                                            dtype=int)


def get_category_crazy_count(dt=None, days=None):
    """
    板块情绪统计（竞价/涨停/炸板/跌停/自然涨停/跌停翘板数）
    """
    return request_json_dataframe_days_date(CATEGORY_CRAZY_COUNT_URL,
                                            dt, days,
                                            dims=2,
                                            columns=['date', 'category', 'zt', 'zb', 'dt', 'zz', 'qb'],
                                            index=['date', 'category'],
                                            dtype=int)


# =========================================================

def get_market_count(dt=None, days=None):
    """
    涨跌停数明细
    """
    rs = request_json_obj_days_date(MARKET_COUNT_URL, dt, days, True)
    if rs is None:
        return None

    df = None
    if days is None:
        data = rs
        df = pd.DataFrame(index=data.time)
        df['zt'] = data.zt
        df['dt'] = data.dt
        df['zz'] = data.zz
    else:
        data = None
        for d in rs:
            b = np.array(d.zz)
            b = np.c_[d.dt, b]
            b = np.c_[d.zt, b]
            b = np.c_[d.time, b]
            a = np.repeat(d.date, len(b))
            if data is None:
                data = np.c_[a, b]
            else:
                data = np.r_[data, np.c_[a, b]]
        if data is None:
            return None
        df = pd.DataFrame(data, columns=['date', 'time', 'zt', 'dt', 'zz'])
        df.set_index(['date', 'time'], inplace=True)

    df = df.astype(int)
    df.index.name = None
    return df


def _get_market_money(url, dt=None, days=None):
    """
    主力资金净额
    """
    rs = request_json_obj_days_date(url, dt, days, True)
    if rs is None:
        return None

    df = None
    if days is None:
        data = rs
        df = pd.DataFrame(index=data.time)
        df['money'] = data.money
    else:
        data = None
        for d in rs:
            b = np.array(d.money)
            b = np.c_[d.time, b]
            a = np.repeat(d.date, len(b))
            if data is None:
                data = np.c_[a, b]
            else:
                data = np.r_[data, np.c_[a, b]]
        if data is None:
            return None
        df = pd.DataFrame(data, columns=['date', 'time', 'money'])
        df.set_index(['date', 'time'], inplace=True)

    df = df.astype(float)
    df.index.name = None
    return df


def get_market_money(dt=None, days=None):
    """
    主力资金净额
    """
    return _get_market_money(MARKET_MONEY_URL, dt, days)


def get_market_money_hgt(dt=None, days=None):
    """
    沪股通资金净额
    """
    return _get_market_money(MARKET_MONEY_HGT_URL, dt, days)


def get_market_money_sgt(dt=None, days=None):
    """
    深股通资金净额
    """
    return _get_market_money(MARKET_MONEY_SGT_URL, dt, days)


def get_market_rate(key, dt=None, days=None):
    """
    上证指数涨跌幅
    """
    rs = request_json_obj_days_date(MARKET_RATE_URL + key, dt, days, True)
    if rs is None:
        return None

    df = None
    if days is None:
        data = rs
        df = pd.DataFrame(index=data.time)
        df['rate'] = data.rate
    else:
        data = None
        for d in rs:
            b = np.array(d.rate)
            b = np.c_[d.time, b]
            a = np.repeat(d.date, len(b))
            if data is None:
                data = np.c_[a, b]
            else:
                data = np.r_[data, np.c_[a, b]]
        if data is None:
            return None
        df = pd.DataFrame(data, columns=['date', 'time', 'rate'])
        df.set_index(['date', 'time'], inplace=True)

    df = df.astype(float)
    df.index.name = None
    return df


def get_market_rate_sh(dt=None, days=None):
    """
    上证指数涨跌幅
    """
    return get_market_rate('sh', dt, days)


def get_market_rate_sz(dt=None, days=None):
    """
    深证指数涨跌幅
    """
    return get_market_rate('sz', dt, days)


def get_market_rate_cy(dt=None, days=None):
    """
    创业指数涨跌幅
    """
    return get_market_rate('cy', dt, days)


def get_market_rate_zt(dt=None, days=None):
    """
    昨日涨停涨跌幅
    """
    return get_market_rate('zt', dt, days)


def get_market_rate_qz(dt=None, days=None):
    """
    权重指数涨跌幅
    """
    return get_market_rate('qz', dt, days)


def get_market_rate_zx(dt=None, days=None):
    """
    中小盘指数涨跌幅
    """
    return get_market_rate('zx', dt, days)


def get_market_order(key, dt=None, days=None):
    """
    上证委买委卖
    """
    rs = request_json_obj_days_date(MARKET_ORDER_URL + key, dt, days, True)
    if rs is None:
        return None

    df = None
    if days is None:
        data = rs
        df = pd.DataFrame(index=data.time)
        df['buy'] = data.buy
        df['sell'] = data.sell
        df['volume'] = data.volume
    else:
        data = None
        for d in rs:
            b = np.array(d.volume)
            b = np.c_[d.sell, b]
            b = np.c_[d.buy, b]
            b = np.c_[d.time, b]
            a = np.repeat(d.date, len(b))
            if data is None:
                data = np.c_[a, b]
            else:
                data = np.r_[data, np.c_[a, b]]
        if data is None:
            return None
        df = pd.DataFrame(data, columns=['date', 'time', 'buy', 'sell', 'volume'])
        df.set_index(['date', 'time'], inplace=True)

    df = df.astype(float)
    df.index.name = None
    return df


def get_market_order_sh(dt=None, days=None):
    """
    上证委买委卖
    """
    return get_market_order('sh', dt, days)


def get_market_order_sz(dt=None, days=None):
    """
    深证委买委卖
    """
    return get_market_order('sz', dt, days)


def get_market_order_cy(dt=None, days=None):
    """
    创业委买委卖
    """
    return get_market_order('cy', dt, days)
