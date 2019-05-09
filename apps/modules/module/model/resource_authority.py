#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:32
# @Author  : liupan
# @Site    : 
# @File    : dict_api.py
# @Software: PyCharm

from apps.core.db.mysql import db
from apps.core.model.base_model import BaseModel


class ResourceAuthority(BaseModel):
    __tablename__ = 'sys_resource_authority'

    role_id = db.Column(db.String(32), nullable=False)
    resource_id = db.Column(db.String(32))
    resource_type = db.Column(db.String(255))

    _default_fields = ["id", "del_flag", "crt_time", "role_id", "resource_id", "resource_type"]

    def __repr__(self):
        return '<ResourceAuthority %r>' % self.resource_type
