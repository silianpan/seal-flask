#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 17:24
# @Author  : liupan
# @Site    : 
# @File    : dict_api.py
# @Software: PyCharm

from flask import request, json
from flask_jwt_extended import jwt_required
from apps.core.blueprint import api
from apps.modules.dict.service import dict_service
from apps.core.rb import Rb


# 获取所有字典分组
@api.route('/ehr/dict/dictGroup/page', methods=['POST'])
@jwt_required
def page_dict_group():
    return Rb.ok(json.loads(dict_service.page_dict_group(request.json)))


@api.route('/ehr/dict/dictItem/all', methods=['POST'])
@jwt_required
def find_all_dict_item():
    return Rb.ok(json.loads(dict_service.find_all_dict_item(request.json)))

