#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import request
from apps.core.flask.login_manager import osr_login_required

from apps.configs.sys_config import METHOD_WARNING
from apps.core.blueprint import api
from apps.core.flask.permission import permission_required
from apps.core.flask.response import response_format
from apps.modules.report.process.comment_access import comment_access


__author__ = "Allen Woo"
@api.route('/admin/comment/access', methods=['GET'])
@osr_login_required
@permission_required()
def api_comment_access():
    """
    GET:
        获取comment数据统计
        days:<int>

    """
    if request.c_method == "GET":
        data = comment_access()
    else:
        data = {"msg_type": "w", "msg": METHOD_WARNING, "http_status": 405}
    return response_format(data)
