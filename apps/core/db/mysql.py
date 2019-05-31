#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:13
# @Author  : liupan
# @Site    : 
# @File    : mysql.py
# @Software: PyCharm

from flask_sqlalchemy import SQLAlchemy
from apps.app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/seal_admin?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)
