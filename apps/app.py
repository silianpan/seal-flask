#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 21:52
# @Author  : liupan
# @Site    : 
# @File    : app.py
# @Software: PyCharm

from flask import Flask
from flask_jwt_extended import JWTManager
import apps.configs.app_config as configs
app = Flask(__name__)

app.config.from_object(configs)

# Setup the Flask-JWT-Extended extension
# app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)
