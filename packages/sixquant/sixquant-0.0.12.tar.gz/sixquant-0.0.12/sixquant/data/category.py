# -*- coding: UTF-8 -*-

from ..constants import CATEGORIES_HEATMAP_URL,CRAZY_HEATMAP_URL
from ..utils.request import request_json_obj_date


def get_categories_heatmap(dt=None):
    """
    板块热图
    """
    return request_json_obj_date(CATEGORIES_HEATMAP_URL, dt)

