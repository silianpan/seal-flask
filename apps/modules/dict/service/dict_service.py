#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:57
# @Author  : liupan
# @Site    : 
# @File    : dict_service.py
# @Software: PyCharm

from flask import json
from apps.core.db.sql_runner import page_query
from apps.modules.dict.model.dict_item import DictItem


def page_dict_group(params={}):
    """分页查询字典分组"""
    sql = '''
    select * from t_dict_group
    '''
    return page_query(sql, params)


def find_all_dict_item(params={}):
    """根据条件查询字典数据"""
    if 'group_code' in params.keys():
        dict_items = DictItem.query.filter_by(group_code=params['group_code']).all()
        result = []
        for dict_item in dict_items:
            result.append(dict_item.to_dict())
        return json.dumps(result)
    return json.dumps([])
