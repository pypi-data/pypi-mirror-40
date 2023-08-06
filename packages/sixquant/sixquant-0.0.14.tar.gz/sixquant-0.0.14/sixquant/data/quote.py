# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
import talib

from ..constants import QUOTE_DAILY, QUOTES_BASIC_DAILY, QUOTES_QUANT_DAILY
from ..utils.datetime_utils import int_date_to_str
from ..utils.exceptions import IllegalArgumentError
from ..utils.request import request_json_obj_days_date, request_json_obj_date


def get_quote(code, days=20, dt=None,
              fields=['pt', 'turnover',
                      'close', 'open', 'high', 'low',
                      'volume', 'money',
                      'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma120'
                      ],
              sma=True):
    """
    日线
    """
    if len(code) != 6:
        raise IllegalArgumentError("get_quote(" + code + ")")

    rs = request_json_obj_days_date(QUOTE_DAILY + "/" + code, dt, days, False)
    if rs is None or len(rs[0]) == 0:
        df = pd.DataFrame([], columns=['date',
                                       'pt', 'turnover',
                                       'close', 'open', 'high', 'low',
                                       'volume', 'money',
                                       'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma120'])
        df.set_index('date', inplace=True)
        df = df.astype(float)
        df.index.name = None
        return df[fields]

    df = pd.DataFrame(rs[0], columns=['date', 'open', 'high', 'low', 'pt', 'turnover', 'volume', 'money', 'factor'])
    df['date'] = df['date'].apply(int_date_to_str)
    df.set_index('date', inplace=True)
    df = df.astype(float)
    df.index.name = None

    n = len(df)
    if days > n:
        days = n  # 服务端也许不能提供足够天数的数据

    # 前复权
    factor = df['factor'].values[0]
    if factor == 0:
        print('data error: get_quote(' + code + ') factor is 0')
        factor = 1.0
    # factor = factor.fillna(1)
    prices = np.round(np.array(rs[1]) / factor, 2)
    df['open'] = np.round(df['open'] / factor, 2)
    df['high'] = np.round(df['high'] / factor, 2)
    df['low'] = np.round(df['low'] / factor, 2)

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


def get_quotes(dt=None, fields=['close', 'open', 'high', 'low',
                                'pt', 'turnover',
                                'volume', 'volume_mean',
                                'money', 'money_mean',
                                'major_money', 'major_buy',
                                'rate',
                                'turn_pt', 'turn_days',
                                'zd', 'ac', 'ac_days', 'bt_days']):
    """
    所有股票
    """
    rs = request_json_obj_date(QUOTES_BASIC_DAILY, dt)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['code',
                                   'close', 'open', 'high', 'low',
                                   'pt', 'turnover',
                                   'volume', 'money',
                                   'factor'])
    df.set_index('code', inplace=True)

    if len(df) > 0:
        factor = df['factor'].values
        df['close'] = np.round(df['close'] / factor, 2)
        df['open'] = np.round(df['open'] / factor, 2)
        df['high'] = np.round(df['high'] / factor, 2)
        df['low'] = np.round(df['low'] / factor, 2)

    if 'turn_pt' in fields \
            or 'turn_days' in fields \
            or 'volume_mean' in fields \
            or 'money_mean' in fields \
            or 'major_money' in fields \
            or 'major_money' in fields \
            or 'rate' in fields \
            or 'zd' in fields \
            or 'ac' in fields \
            or 'ac_days' in fields \
            or 'bt_days' in fields:
        rs2 = request_json_obj_date(QUOTES_QUANT_DAILY, dt)
        if rs2 is None:
            rs2 = []

        df2 = pd.DataFrame(rs2, columns=['code',
                                         'turn_pt', 'turn_days',
                                         'volume_mean',
                                         'money_mean',
                                         'major_money', 'major_buy',
                                         'rate',
                                         'zd', 'ac', 'ac_days', 'bt_days'])
        df2.set_index('code', inplace=True)
        for field in fields:
            if field in df2.columns:
                df[field] = df2[field]

    df = df.astype(float)
    if 'turn_days' in df.columns:
        df['turn_days'] = df['turn_days'].fillna(0).astype(int)
    if 'zd' in df.columns:
        df['zd'] = df['zd'].fillna(0).astype(int)
    if 'ac' in df.columns:
        df['ac'] = df['ac'].fillna(0).astype(int)
    if 'ac_days' in df.columns:
        df['ac_days'] = df['ac_days'].fillna(0).astype(int)
    if 'bt_days' in df.columns:
        df['bt_days'] = df['bt_days'].fillna(0).astype(int)

    df.index.name = None
    df.sort_index(axis=0, ascending=True, inplace=True)
    return df[fields].copy()
