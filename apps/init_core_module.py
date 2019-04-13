#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 16:58
# @Author  : liupan
# @Site    : 
# @File    : init_core_module.py
# @Software: PyCharm

from apps.core.blueprint import api

"""
初始化核心模块
"""


def init_core_module(app):
    app.register_blueprint(api)
