#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:57
# @Author  : liupan
# @Site    : 
# @File    : user_service.py
# @Software: PyCharm

from flask import json
from apps.modules.user.model.user import User


def list_user():
    return json.dumps([user.to_dict() for user in User.query.all()])
