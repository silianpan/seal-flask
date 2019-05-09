#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 17:24
# @Author  : liupan
# @Site    : 
# @File    : dict_api.py
# @Software: PyCharm

from flask import json
from flask_jwt_extended import jwt_required
from apps.core.blueprint import api
from apps.modules.modules.service import modules_service
from apps.core.rb import Rb


@api.route('/admin/module/find/by/pid/<pid>', methods=['GET'])
@jwt_required
def find_modules_by_pid(pid):
    return Rb.ok(json.loads(modules_service.find_modules_by_pid(pid)))
