# -*- coding: UTF-8 -*-

import pandas as pd

from ..constants import MONEY_DAILY
from ..utils.datetime_utils import int_date_to_str
from ..utils.request import request_json_obj_days_date


def get_money(days=10, dt=None):
    """
    资金净额
    """
    rs = request_json_obj_days_date(MONEY_DAILY, dt, days, False)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['date', 'a', 'hgt', 'sgt'])
    df['date'] = df['date'].apply(int_date_to_str)
    df.set_index('date', inplace=True)
    df = df.astype(float)
    df.index.name = None

    return df
