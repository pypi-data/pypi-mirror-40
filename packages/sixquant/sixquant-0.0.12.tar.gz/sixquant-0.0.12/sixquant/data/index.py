# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
import talib

from ..constants import INDEX_DAILY, INDEX_MINUTELY_SH, INDEX_MINUTELY_SZ, INDEX_MINUTELY_CY
from ..utils.datetime_utils import int_date_to_str
from ..utils.exceptions import IllegalArgumentError
from ..utils.request import request_json_obj_days_date


def get_index(code, days=20, dt=None,
              fields=['pt', 'money', 'close', 'open', 'high', 'low',
                      'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma120'
                      ],
              sma=True):
    """
    指数日线
    """
    rs = request_json_obj_days_date(INDEX_DAILY + "/" + code, dt, days, False)
    if rs is None or len(rs[0]) == 0:
        return None

    df = pd.DataFrame(rs[0], columns=['date', 'open', 'high', 'low', 'pt', 'money'])
    df['date'] = df['date'].apply(int_date_to_str)
    df.set_index('date', inplace=True)
    df = df.astype(float)
    df.index.name = None

    n = len(df)
    if days > n:
        days = n  # 服务端也许不能提供足够天数的数据

    prices = np.array(rs[1])

    df['close'] = prices[-days:]

    if sma:
        # 算数移动均线SMA
        df['ma5'] = np.round(talib.MA(prices, 5, matype=0)[-days:], 2)
        df['ma10'] = np.round(talib.MA(prices, 10, matype=0)[-days:], 2)
        df['ma20'] = np.round(talib.MA(prices, 20, matype=0)[-days:], 2)
        df['ma30'] = np.round(talib.MA(prices, 30, matype=0)[-days:], 2)
        df['ma60'] = np.round(talib.MA(prices, 60, matype=0)[-days:], 2)
        df['ma120'] = np.round(talib.MA(prices, 120, matype=0)[-days:], 2)

    return df[fields].copy()


def get_index_sh(dt=None, days=None, sma=True):
    return get_index('sh', dt, days, sma)


def get_index_sz(dt=None, days=None, sma=True):
    return get_index('sz', dt, days, sma)


def get_index_cy(dt=None, days=None, sma=True):
    return get_index('cy', dt, days, sma)


def get_index_hs(dt=None, days=None, sma=True):
    return get_index('hs', dt, days, sma)


def get_index_300(dt=None, days=None, sma=True):
    return get_index('300', dt, days, sma)


def get_index_50(dt=None, days=None, sma=True):
    return get_index('50', dt, days, sma)


# =========================================================

def get_index_minutely(key, dt=None, days=None):
    """
    指数分时
    """
    if key.lower() == 'sh':
        key = INDEX_MINUTELY_SH
    elif key.lower() == 'sz':
        key = INDEX_MINUTELY_SZ
    elif key.lower() == 'cy':
        key = INDEX_MINUTELY_CY
    else:
        raise IllegalArgumentError("get_index_minutely(" + key + ")")
    rs = request_json_obj_days_date(key, dt, days, True)
    if rs is None:
        return None

    if days is None:
        data = rs.data
        df = pd.DataFrame(data, columns=['time', 'value', 'mean', 'volume', 'o'])
        df.set_index('time', inplace=True)
    else:
        data = None
        for d in rs:
            b = np.array(d.data)
            a = np.repeat(d.date, len(b))
            if data is None:
                data = np.c_[a, b]
            else:
                data = np.r_[data, np.c_[a, b]]
        if data is None:
            return None
        df = pd.DataFrame(data, columns=['date', 'time', 'value', 'mean', 'volume', 'o'])
        df.set_index(['date', 'time'], inplace=True)

    df[['value', 'mean', 'volume']] = df[['value', 'mean', 'volume']].astype(float)
    df['o'] = df['o'].astype(int)
    df.index.name = None
    return df


def get_index_minutely_sh(dt=None, days=None):
    return get_index_minutely('sh', dt, days)


def get_index_minutely_sz(dt=None, days=None):
    return get_index_minutely('sz', dt, days)


def get_index_minutely_cy(dt=None, days=None):
    return get_index_minutely('cy', dt, days)


def get_index_minutely_hs(dt=None, days=None):
    return get_index_minutely('hs', dt, days)


def get_index_minutely_300(dt=None, days=None):
    return get_index_minutely('300', dt, days)


def get_index_minutely_50(dt=None, days=None):
    return get_index_minutely('50', dt, days)
