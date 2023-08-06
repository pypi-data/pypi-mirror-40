# coding=utf-8

import json
from collections import namedtuple


def _json_object_hook(d): return namedtuple('_', d.keys())(*d.values())


# json 字符串转 object
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
