#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:32
# @Author  : liupan
# @Site    : 
# @File    : user_api.py
# @Software: PyCharm

from apps.core.db.mysql import db
from apps.core.model.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'sys_user'

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255))
    pwd = db.Column(db.String(255))
    salt = db.Column(db.String(50))
    dept_id = db.Column(db.String(32))
    user_no = db.Column(db.String(32))
    phone = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    enable = db.Column(db.Boolean)
    lock_status = db.Column(db.Boolean)
    photo = db.Column(db.Text)
    del_flag = db.Column(db.Boolean)
    crt_name = db.Column(db.String(255))
    crt_user = db.Column(db.String(255))
    upd_name = db.Column(db.String(255))
    upd_user = db.Column(db.String(255))
    crt_time = db.Column(db.DateTime)
    upd_time = db.Column(db.DateTime)
    version = db.Column(db.Integer)

    _default_fields = ["name", "username", "salt", "dept_id", "phone", "mail", "enable", "lock_status", "photo"]

    def __repr__(self):
        return '<User %r>' % self.username
