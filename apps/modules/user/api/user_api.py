#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 17:24
# @Author  : liupan
# @Site    : 
# @File    : user_api.py
# @Software: PyCharm

from flask import request, jsonify, json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from apps.core.blueprint import api
from apps.modules.user.service import user_service
from apps.core.util import match_password
from apps.core.tools import to_tree
from apps.core.rb import Rb
# from apps.core.helper.cache import cached
# from apps.core.helper.protected import protected
# from apps.core.helper.rate_limited import rate_limited


@api.route('/auth/jwt/token', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "参数错误，不是json格式"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return Rb.failed('用户名参数错误')
    if not password:
        return Rb.failed('密码参数错误')

    # 查询数据库用户名和密码
    user = user_service.query_by_username(username)
    if user is None:
        return Rb.failed('该用户不存在')

    if match_password(password, user.pwd):
        access_token = create_access_token(identity=username)
        return Rb.ok(access_token)
    return Rb.failed('用户名或密码不正确')


# 获取所有用户
@api.route('/user/all', methods=['GET'])
@jwt_required
# @rate_limited(limit=50, minutes=60)  # only 50 requests from user/ip to this endpoint allowed per hour
# @protected(limit=2, minutes=720)  # only 2 404 requests from same ip to this endpoint allowed per 12 hours
# @cached(minutes=5)  # response cached for 5 minutes
def list_user():
    return user_service.list_user()


@api.route('/admin/user/front/info', methods=['GET'])
@jwt_required
def get_current_user():
    current_user = get_jwt_identity()
    # 查询用户
    user = user_service.query_by_username(current_user)
    user = user.to_dict()
    # 查询菜单
    menus = user_service.query_auth_modules({'user_id': user['id'], 'resource_type': 'menu'})
    menus_tree = to_tree(json.loads(menus))
    user['menus'] = menus_tree
    elements = user_service.query_auth_modules_element({'user_id': user['id'], 'resource_type': 'btn'})
    user['elements'] = json.loads(elements)
    # 查询权限
    return Rb.ok(user)


@api.route('/module', methods=['POST'])
def query_modules():
    if not request.json:
        return "request parms invalid!", 400
    return user_service.query_modules(request.json)
