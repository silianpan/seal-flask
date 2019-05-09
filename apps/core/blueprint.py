#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 16:50
# @Author  : liupan
# @Site    :
# @File    : blueprint.py
# @Software: PyCharm

from importlib import import_module
from flask import Blueprint
from apps.configs.sys_config import API_URL_PREFIX

api = Blueprint('api', __name__, url_prefix=API_URL_PREFIX)

routing_modules = [
    {
        "from": "apps.modules.user.api",
        "import": ["user_api"]
    },
    {
        "from": "apps.modules.dict.api",
        "import": ["dict_api"]
    },
    {
        "from": "apps.modules.module.api",
        "import": ["module_api"]
    },
    {
        "from": "apps.modules.role.api",
        "import": ["role_api"]
    }
]

for rout_m in routing_modules:
    for im in rout_m["import"]:
        module = "{}.{}".format(rout_m["from"], im)
        import_module(module)
