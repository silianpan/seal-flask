#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 17:24
# @Author  : liupan
# @Site    : 
# @File    : user_api.py
# @Software: PyCharm

from flask import request
from apps.core.blueprint import api
from apps.modules.user.service import user_service
# from apps.core.helper.cache import cached
# from apps.core.helper.protected import protected
# from apps.core.helper.rate_limited import rate_limited


# 获取所有用户
@api.route('/user/all', methods=['GET'])
# @rate_limited(limit=50, minutes=60)  # only 50 requests from user/ip to this endpoint allowed per hour
# @protected(limit=2, minutes=720)  # only 2 404 requests from same ip to this endpoint allowed per 12 hours
# @cached(minutes=5)  # response cached for 5 minutes
def list_user():
    return user_service.list_user()


@api.route('/module', methods=['POST'])
def query_modules():
    if not request.json:
        return "request parms invalid!", 400
    return user_service.query_modules(request.json)
