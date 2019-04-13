#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:57
# @Author  : liupan
# @Site    : 
# @File    : user_service.py
# @Software: PyCharm

from flask import jsonify
from apps.modules.user.model.user import User


def list_user():
    users = User.query.all()
    temp = []
    for x in users:
        temp.append(x.to_json())
    return jsonify(temp)
