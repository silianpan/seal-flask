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
from apps.modules.module.service import module_service
from apps.core.rb import Rb


@api.route('/admin/module/find/by/pid/<pid>', methods=['GET'])
@jwt_required
def find_module_by_pid(pid):
    return Rb.ok(json.loads(module_service.find_module_by_pid(pid)))


@api.route('/admin/module/find/authority/by/role/and/pid', methods=['GET'])
@jwt_required
def find_module_and_element_by_role_pid():
    role_id = request.args.get('roleId')
    pid = request.args.get('pid')
    modules = module_service.find_module_by_role_pid(role_id, pid)
    elements = module_service.find_element_by_role_module(role_id, pid)
    modules = json.loads(modules)
    elements = json.loads(elements)
    modules.extend(elements)
    print(modules)
    return Rb.ok(modules)


@api.route('/admin/resourceAuthority/logic/delete', methods=['DELETE'])
@jwt_required
def logic_del_resource_authority():
    """逻辑删除资源权限"""
    return Rb.ok(module_service.logic_del_resource_authority(request.args.get('id')))


@api.route('/admin/module/sign/authority', methods=['POST'])
@jwt_required
def sign_authority():
    """赋予角色权限"""
    ret = module_service.sign_authority(request.json)
    if not ret:
        return Rb.failed('权限已经存在')
    return Rb.ok(ret)
