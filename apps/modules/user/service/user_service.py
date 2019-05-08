#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:57
# @Author  : liupan
# @Site    : 
# @File    : user_service.py
# @Software: PyCharm

from apps.modules.user.model.user import User
from apps.core.db.sql_runner import build_sql, execute_real_sql, page_query


# 更加用户名和密码查询用户
def query_by_username(username):
    return User.query.filter_by(username=username).first()


def page_user(params={}):
    """分页查询用户"""
    sql = '''
    select * from sys_user
    '''
    return page_query(sql, params)


def query_auth_modules(params={}):
    """查询权限模块"""
    sql = """
    SELECT
            m.*
        FROM
            sys_module m,
            sys_resource_authority ra
        WHERE
            ra.resource_id = m.id
          AND ra.del_flag = 0
          AND m.del_flag = 0
          AND m.`enable` = 1
          { and ra.resource_type = :resource_type }
          AND EXISTS (
                SELECT
                    rr.id
                FROM
                    sys_re_role_user rr,
                    sys_user u
                WHERE
                    rr.del_flag = 0
                  AND u.del_flag = 0
                  and u.`enable` = 1
                  AND rr.user_id = u.id
                  and rr.role_id = ra.role_id
                  { AND u.id = :user_id }
            )
        ORDER BY
            m.LEVEL
    """
    real_sql = build_sql(sql, params)
    return execute_real_sql(real_sql)


def query_auth_modules_element(params={}):
    """查询权限模块元素"""
    sql = """
    SELECT
        e.*
    FROM
        sys_module_element e,
        sys_resource_authority ra
    WHERE
        ra.resource_id = e.id
      AND ra.del_flag = 0
      AND e.del_flag = 0
      AND e.`enable` = 1
      { AND ra.resource_type = :resource_type }
      AND EXISTS (
            SELECT
                rr.id
            FROM
                sys_re_role_user rr,
                sys_user u
            WHERE
                rr.del_flag = 0
              AND u.del_flag = 0
              and u.`enable` = 1
              AND rr.user_id = u.id
              and rr.role_id = ra.role_id
              { AND u.id = :user_id }
        )

    ORDER BY
        e.LEVEL
    """
    real_sql = build_sql(sql, params)
    return execute_real_sql(real_sql)
