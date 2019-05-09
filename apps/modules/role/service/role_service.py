#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:57
# @Author  : liupan
# @Site    : 
# @File    : dict_service.py
# @Software: PyCharm

from apps.core.db.sql_runner import page_query


def page_role(params={}):
    """分页查询角色"""
    sql = '''
    select * from sys_role
    '''
    return page_query(sql, params)
