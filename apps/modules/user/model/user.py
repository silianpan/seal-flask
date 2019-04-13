#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:32
# @Author  : liupan
# @Site    : 
# @File    : user.py
# @Software: PyCharm

from apps.core.db.mysql import db


class User(db.Model):
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

    def __repr__(self):
        return '<User %r>' % self.username

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username
        }
