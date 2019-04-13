# -*-coding:utf-8-*-
import time
"""
web初始化数据
条件:涉及的collection没有数据的时候, 将自动初始化.
或涉及的collection没有符合数据condition的数据的时候, 将自动初始化
"""
INIT_DATAS = [
    {
        "db": "osr_web",
        "coll": "category",
        "datas": [{"name": "风景", "type": "image", "user_id": 0},
                  {"name": "城市", "type": "image", "user_id": 0}]
    },

    {
        "db": "osr_sys",
        "coll": "audit_rules",
        "datas": [{"time": time.time(), "rule": "osroom", "project": "username"},
                  {"time": time.time(), "rule": ".*管理员.*", "project": "username"},
                  {"time": time.time(), "rule": ".*管理员.*", "project": "class_name"}]
    },

    {
        "db": "osr_user",
        "coll": "permission",
        "datas": [
            {"value": 2147483648, "name": "ROOT",
                "is_default": 1, "explain": "超级管理, 有权控制ADMIN分配"},
            {"value": 134217728, "name": "ADMIN",
                "is_default": 1, "explain": "普通管理员"},
            {"value": 0b10,
             "name": "STAFF",
             "is_default": 0,
             "explain": "用于识别工作人员识别"},
            {"value": 1, "name": "GENERAL_USER",
                "is_default": 0, "explain": "普通用户权重"},
            {"value": 0b100, "name": "TEST", "is_default": 0, "explain": "示范例子,你可以自己创建更多权权重"}]
    },

    {
        "db": "osr_sys",
        "coll": "sys_urls",
        "condition": {"type": "page"},
        "datas": [
            {"url": "/osr-admin", "endpoint": "", "type": "page", "methods": ["GET"], "create": "auto",
             "custom_permission": {"GET": 0b10}, "login_auth": {"GET": 1}},
            {"url": "/osr-admin/user", "endpoint": "", "type": "page", "methods": ["GET"], "create": "auto",
             "custom_permission": {"GET": 0b10}, "login_auth": {"GET": 1}},
            {"url": "/osr-admin/role", "endpoint": "", "type": "page", "methods": ["GET"], "create": "auto",
             "custom_permission": {"GET": 0b10}, "login_auth": {"GET": 1}},
            {"url": "/osr-admin/plugin", "endpoint": "", "type": "page", "methods": ["GET"], "create": "auto",
             "custom_permission": {"GET": 0b10}, "login_auth": {"GET": 1}},
            {"url": "/osr-admin/post", "endpoint": "", "type": "page", "methods": ["GET"], "create": "auto",
             "custom_permission": {"GET": 0b10}, "login_auth": {"GET": 1}},
            {"url": "/osr-admin/comment", "endpoint": "", "type": "page", "methods": ["GET"], "create": "auto",
             "custom_permission": {"GET": 0b10}, "login_auth": {"GET": 1}},
        ]
    }
]
