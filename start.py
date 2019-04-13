#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 16:50
# @Author  : liupan
# @Site    :
# @File    : start.py
# @Software: PyCharm

from flask import Flask
from flask_script import Manager
from apps.init_core_module import init_core_module

app = Flask(__name__)
# 初始化核心模块
init_core_module(app)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
