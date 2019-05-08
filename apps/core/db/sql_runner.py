#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-04 12:39
# @Author  : liupan
# @Site    : 
# @File    : sql_runner.py
# @Software: PyCharm
from flask import json
from sqlalchemy.sql import text
from apps.core.db.mysql import db
from apps.core.tools import CustomEncoder


def execute_real_sql(real_sql):
    """执行真正的sql"""
    result = db.engine.execute(text(real_sql)).fetchall()
    return json.dumps([dict(r) for r in result], cls=CustomEncoder)


def execute_real_sql_dict(real_sql):
    """执行真正的sql, 返回字典"""
    result = db.engine.execute(text(real_sql)).fetchall()
    return [dict(r) for r in result]


def to_dict_dumps(result):
    """转换为字典"""
    return json.dumps([dict(r) for r in result], cls=CustomEncoder)


def page_query(sql='', params={}):
    """分页查询"""
    page_index = 1
    page_size = 10
    if 'current' in params.keys():
        page_index = int(params['current'])
    if 'size' in params.keys():
        page_size = int(params['size'])
    return page(page_index, page_size, sql, params)


def page(page_index=1, page_size=10, sql='', params={}):
    """分页查询"""
    if page_index <= 0:
        page_index = 1
    result = {
        'total': 0,
        'records': [],
        'current': page_index,
        'size': page_size
    }
    real_sql = build_sql(sql, params)
    count_sql = build_count_sql(real_sql)
    res_count = execute_real_sql_dict(count_sql)
    if len(res_count) > 0:
        result['total'] = res_count[0]['total']
    page_sql = build_page_sql(real_sql, {'current': page_index, 'size': page_size})
    res = execute_real_sql_dict(page_sql)
    result['records'] = res
    return json.dumps(result, cls=CustomEncoder)


def build_sql(sql='', params={}):
    """组装sql"""
    stack = []
    real_sql = []
    i = 0
    for ch in sql:
        if ch == '{':
            stack.append(i)
        elif ch == '}':
            start_index = stack.pop()
            target = sql[start_index:i+1]
            is_find = False
            if params:
                for key, value in params.items():
                    field = ':' + key
                    if field in target:
                        is_find = True
                        target = target.replace(str(field), "'" + str(value) + "'")

            if is_find:
                target = target.replace('{', '')
                target = target.replace('}', '')
                real_sql.extend(target)
        else:
            if len(stack) == 0:
                real_sql.append(ch)
        i = i + 1
    return ''.join(real_sql)


def build_page_sql(sql='', options={'current': 1, 'size': 10}):
    """组装分页sql"""
    current = options['current']
    size = options['size']
    offset = (current - 1) * size
    return sql + ' limit ' + str(offset) + ',' + str(size)


def build_count_sql(sql=''):
    """组长查询总数sql"""
    sql = sql.lower()
    return 'select count(1) as total ' + sql[sql.find('from'):]
