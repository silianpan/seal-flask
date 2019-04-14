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
