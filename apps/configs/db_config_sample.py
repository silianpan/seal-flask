# -*-coding:utf-8-*-
__author__ = "Allen Woo"
DB_CONFIG = {
    "mongodb": {
        "mongo_web": {
            "username": "root",
            "config": {
                "fsync": False,
                "replica_set": None
            },
            "dbname": "osr_web",
            "host": [
                "127.0.0.1:27017"
            ],
            "password": "<Your password>"
        },
        "mongo_user": {
            "username": "root",
            "config": {
                "fsync": False,
                "replica_set": None
            },
            "dbname": "osr_user",
            "host": [
                "127.0.0.1:27017"
            ],
            "password": "<Your password>"
        },
        "mongo_sys": {
            "username": "root",
            "config": {
                "fsync": False,
                "replica_set": None
            },
            "dbname": "osr_sys",
            "host": [
                "127.0.0.1:27017"
            ],
            "password": "<Your password>"
        }
    },
    "redis": {
        "host": [
            "127.0.0.1"
        ],
        "password": "<Your password>",
        "port": [
            "6379"
        ]
    }
}
