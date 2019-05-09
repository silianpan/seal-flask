#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:57
# @Author  : liupan
# @Site    : 
# @File    : dict_service.py
# @Software: PyCharm

from apps.core.db.sql_runner import build_sql, execute_real_sql


def find_module_by_pid(pid):
    """根据pid查询模块"""
    params = {'pid': pid}
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


def find_module_by_role_pid(role_id, pid):
    """根据角色id和pid查询模块"""
    params = {'role_id': role_id, 'pid': pid}
    sql = '''
    SELECT
        m.*,
        ( SELECT count( sm.id ) FROM sys_module sm WHERE sm.del_flag = 0 AND sm.pid = m.id ) children_cnt,
        ( SELECT count( e.id ) FROM sys_module_element e WHERE e.del_flag = 0 AND e.module_id = m.id ) ele_cnt,
        re.role_id,
        re.id authority_id
    FROM
        sys_module m
            LEFT JOIN sys_resource_authority re ON re.resource_id = m.id and re.del_flag = 0
            { AND re.role_id = :role_id }
    WHERE
        m.del_flag = 0
      { AND m.pid = :pid }
    ORDER BY
        m.`level`,
        children_cnt
    '''
    real_sql = build_sql(sql, params)
    return execute_real_sql(real_sql)


def find_element_by_role_module(role_id, module_id):
    """根据角色id和模块id查询模块元素"""
    params = {'role_id': role_id, 'module_id': module_id}
    sql = '''
    SELECT
        e.*,
        re.role_id,
        re.id authority_id
    FROM
        sys_module_element e
            LEFT JOIN sys_resource_authority re ON re.resource_id = e.id
            AND re.del_flag= 0 
            { and  re.role_id = :role_id }
    WHERE
        e.del_flag = 0
      { AND e.module_id = :module_id }
    ORDER BY
        e.`level`
    '''
    real_sql = build_sql(sql, params)
    return execute_real_sql(real_sql)
