#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:57
# @Author  : liupan
# @Site    : 
# @File    : user_service.py
# @Software: PyCharm

from flask import json
from sqlalchemy.sql import text
from apps.modules.user.model.user import User
from apps.core.db.mysql import db
from apps.core.tools import CustomEncoder
from apps.core.db.sql_runner import build_sql


# 更加用户名和密码查询用户
def query_by_username(username):
    return User.query.filter_by(username=username).first()


def list_user():
    return json.dumps([user.to_dict() for user in User.query.all()])


def query_modules(params={}):
    sql = """
    SELECT
        m.* 
    FROM
        sys_module m
        INNER JOIN sys_user u ON u.id = m.crt_user 
        AND u.del_flag = 0
        and u.id = :id
    WHERE
        m.del_flag = 0
    """
    result = db.engine.execute(text(sql), params).fetchall()
    return json.dumps([dict(r) for r in result], cls=CustomEncoder)


def query_auth_modules(params={}):
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
    build_sql(sql, {'resource_type': 1, 'user_id': 1})
