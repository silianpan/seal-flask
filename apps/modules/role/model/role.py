#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:32
# @Author  : liupan
# @Site    : 
# @File    : dict_api.py
# @Software: PyCharm

from apps.core.db.mysql import db
from apps.core.model.base_model import BaseModel


class Role(BaseModel):
    __tablename__ = 'sys_role'

    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer)
    pid = db.Column(db.String(32))
    pids = db.Column(db.String(1024))
    desc = db.Column(db.String(255))
    enable = db.Column(db.Boolean)

    _default_fields = ["id", "del_flag", "crt_time", "name", "level", "pid", "desc", "enable"]

    def __repr__(self):
        return '<Role %r>' % self.name
