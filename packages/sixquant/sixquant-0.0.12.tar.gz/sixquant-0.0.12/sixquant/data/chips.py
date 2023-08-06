# -*- coding: UTF-8 -*-

from ..constants import MARKET_CHIPS_URL
from ..utils.request import request_json_dataframe_codes_date
from ..utils.datetime_utils import get_last_trading_day, get_prev_trade_day


def get_chips(codes=None, dt=None):
    """
    筹码
    """
    if dt is None:
        dt = get_prev_trade_day(get_last_trading_day())  # 筹码数据当天没有的，只有前一天有
    df = request_json_dataframe_codes_date(MARKET_CHIPS_URL, codes, dt)
    if df is not None:
        df.set_index('code', inplace=True)
        if 'date' in df.columns:
            df.drop('date', axis=1, inplace=True)
        df.index.name = None

    return df
