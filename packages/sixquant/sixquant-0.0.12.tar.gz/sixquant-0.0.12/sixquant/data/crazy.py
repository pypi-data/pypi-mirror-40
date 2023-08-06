# -*- coding: UTF-8 -*-

import pandas as pd

from ..constants import CRAZY_HEATMAP_URL, CRAZY_DAILY_ZT, CRAZY_DAILY_ZB
from ..utils.request import request_json_obj_date


def get_crazy_heatmap(dt=None, zt=True):
    """
    打板热图
    """
    if zt == False:
        return request_json_obj_date(CRAZY_HEATMAP_URL, dt, "?zt=0")
    return request_json_obj_date(CRAZY_HEATMAP_URL, dt)


def get_crazy_zt_list(dt=None, fields=['price', 'pt', 'turnover',
                                       'major_money', 'buy_money',
                                       'state', 'reason', 'crazy_time',
                                       'continues', 'times', 'days']):
    """
    实时
    """
    rs = request_json_obj_date(CRAZY_DAILY_ZT, dt)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['code', 'price', 'pt',
                                   'turnover', 'major_money', 'buy_money',
                                   'state', 'reason',
                                   'crazy_time', 'crash_time',
                                   'continues', 'times', 'days'
                                   ])
    df.set_index('code', inplace=True)
    df[['price', 'pt', 'turnover', 'major_money', 'buy_money']] = df[
        ['price', 'pt', 'turnover', 'major_money', 'buy_money']].astype(float)
    df[['continues', 'times', 'days']] = df[['continues', 'times', 'days']].astype(int)
    df.index.name = None

    return df[fields].copy()


def get_crazy_zb_list(dt=None, fields=['price', 'pt', 'turnover', 'major_money', 'crash_time']):
    """
    实时
    """
    rs = request_json_obj_date(CRAZY_DAILY_ZB, dt)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['code', 'price', 'pt',
                                   'turnover', 'major_money', 'buy_money',
                                   'state', 'reason',
                                   'crazy_time', 'crash_time',
                                   'continues', 'times', 'days'
                                   ])
    df.set_index('code', inplace=True)
    df[['price', 'pt', 'turnover', 'major_money']] = df[
        ['price', 'pt', 'turnover', 'major_money']].astype(float)
    df.index.name = None

    return df[fields].copy()
