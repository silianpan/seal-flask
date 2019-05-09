#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:32
# @Author  : liupan
# @Site    : 
# @File    : dict_api.py
# @Software: PyCharm

from apps.core.db.mysql import db
from apps.core.model.base_model import BaseModel


class Module(BaseModel):
    __tablename__ = 'sys_module'

    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.String(255))
    code = db.Column(db.String(255))
    type = db.Column(db.String(255))
    pid = db.Column(db.String(32))
    pids = db.Column(db.String(1024))
    path = db.Column(db.String(255))
    route = db.Column(db.String(255))
    config = db.Column(db.String(255))
    icon_cls = db.Column(db.String(255))
    level = db.Column(db.Integer)
    enable = db.Column(db.Boolean)

    _default_fields = ["id", "name", "desc", "code", "type", "pid", "path", "route", "icon_cls", "level", "enable"]

    def __repr__(self):
        return '<Module %r>' % self.name
