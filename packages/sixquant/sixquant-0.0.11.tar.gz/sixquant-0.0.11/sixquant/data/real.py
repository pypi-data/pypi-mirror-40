# -*- coding: UTF-8 -*-

import pandas as pd

from ..constants import QUOTE_REAL
from ..utils.request import request_json_obj


def get_real_quote(code, fields=['pt', 'turnover',
                                 'price', 'open', 'high', 'low',
                                 'money', 'major_money', 'major_buy',
                                 'rate', 'speed']):
    """
    实时
    """
    rs = request_json_obj(QUOTE_REAL + "/" + code)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['code', 'speed', 'price',
                                   'open', 'high', 'low',
                                   'pt', 'turnover',
                                   'money', 'major_money', 'major_buy',
                                   'rate'
                                   ])
    df.set_index('code', inplace=True)
    df = df.astype(float)
    df.index.name = None

    return df[fields].copy()


def get_real_quotes(fields=['pt', 'turnover',
                            'price', 'open', 'high', 'low',
                            'money', 'major_money', 'major_buy',
                            'rate', 'speed']):
    """
    实时
    """
    df = get_real_quote('all', fields)
    df.sort_index(axis=0, ascending=True, inplace=True)
    return df
