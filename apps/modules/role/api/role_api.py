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
from apps.modules.role.service import role_service
from apps.core.rb import Rb


@api.route('/admin/role/page', methods=['POST'])
@jwt_required
def page_role():
    return Rb.ok(json.loads(role_service.page_role(request.json)))
