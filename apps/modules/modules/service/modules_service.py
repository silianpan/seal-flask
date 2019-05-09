#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:57
# @Author  : liupan
# @Site    : 
# @File    : dict_service.py
# @Software: PyCharm

from apps.core.db.sql_runner import build_sql, execute_real_sql


def find_modules_by_pid(pid):
    params = {'pid': pid}
    """根据pid查询模块"""
    sql = '''
    SELECT
        m.*,
        ( SELECT count( sm.id ) FROM sys_module sm WHERE sm.del_flag = 0 AND sm.pid = m.id ) children_cnt
    FROM
        sys_module m
    WHERE
        m.del_flag = 0
      { AND m.pid = :pid }
    ORDER BY
        m.`level` , children_cnt
    '''
    real_sql = build_sql(sql, params)
    return execute_real_sql(real_sql)
