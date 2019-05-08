#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-04 12:39
# @Author  : liupan
# @Site    : 
# @File    : sql_runner.py
# @Software: PyCharm


def build_sql(sql='', params={}):
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


