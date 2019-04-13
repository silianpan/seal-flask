#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 17:24
# @Author  : liupan
# @Site    : 
# @File    : user.py
# @Software: PyCharm


from apps.core.blueprint import api
from flask import jsonify


# 获取所有用户
@api.route('/user/all', methods=['GET'])
def list_user():
    return jsonify({
        "status": 200,
        "data": "liupan"
    })
