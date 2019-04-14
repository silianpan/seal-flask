#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-14 23:15
# @Author  : liupan
# @Site    : 
# @File    : tools.py
# @Software: PyCharm


import json
from datetime import datetime


class CustomEncoder(json.JSONEncoder):
    """A C{json.JSONEncoder} subclass to encode documents that have fields of
        type C{bson.objectid.ObjectId}, C{datetime.datetime}
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)
