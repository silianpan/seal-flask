#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:57
# @Author  : liupan
# @Site    : 
# @File    : dict_service.py
# @Software: PyCharm

from flask import json
from apps.core.db.sql_runner import build_sql, execute_real_sql
from apps.modules.module.model.resource_authority import ResourceAuthority
from apps.core.db.mysql import db


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


def logic_del_resource_authority(id):
    """逻辑删除资源权限"""
    ra = ResourceAuthority.query.filter_by(id=id).first()
    ra.del_flag = 1
    db.session.commit()
    return True


def sign_authority(params={}):
    """赋予角色权限"""
    sql = '''
    select count(1) total from sys_resource_authority ra where ra.del_flag = 0
    { and ra.role_id = :roleId }
    { and ra.resource_id = :resourceId }
    { and ra.resource_type = :resourceType }
    '''
    real_sql = build_sql(sql, params)
    ra_count = execute_real_sql(real_sql)
    ra_count = json.loads(ra_count)
    if len(ra_count) > 0:
        total = ra_count[0]['total']
        if int(total) > 0:
            return False
    ra = ResourceAuthority(role_id=params['roleId'], resource_id=params['resourceId'], resource_type=params['resourceType'], del_flag=0)
    db.session.add(ra)
    db.session.commit()
    return True
