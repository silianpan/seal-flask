# -*-coding:utf-8-*-
import json
import os
from copy import deepcopy
import time
from apps.configs.sys_config import APPS_PATH
from apps.core.logger.web_logging import web_start_log
from init_datas import INIT_DATAS

__author__ = 'Allen Woo'


def update_mdb_collections(mdb_sys, mdb_web, mdb_user):
    """
    更新数据库mongodb collection, 不存在的colletion则创建
    :param mdb_sys:
    :param mdb_web:
    :param mdb_user:
    :return:
    """

    # 读取配置中的数据库json 数据
    with open("{}/configs/collections.json".format(APPS_PATH)) as rf:
        jsondata = rf.read()
        if jsondata:
            collections = json.loads(jsondata)
        else:
            collections = {}

    dbs = {"mdb_sys": mdb_sys,
           "mdb_user": mdb_user,
           "mdb_web": mdb_web
           }

    # 检查数据库collections
    for dbname, colls in collections.items():
        mdb = dbs[dbname]
        for coll in colls:
            try:
                mdb.dbs.create_collection(coll)
                web_start_log.info(
                    "[DB: {}] Create collection '{}'".format(
                        mdb.name, coll))
            except Exception as e:
                if "already exists" in str(e):
                    web_start_log.info(e)
                else:
                    web_start_log.warning(e)

    # 将最新的数据库结构写入配置文件, 方便开发者了解结构
    new_collections = {}
    for dbname, mdb in dbs.items():
        new_collections[dbname] = {}
        collnames = mdb.dbs.collection_names()
        for collname in collnames:
            if collname == "system.indexes" or collname.startswith("plug_"):
                continue
            new_collections[dbname][collname] = {}
            data = mdb.dbs[collname].find_one({}, {"_id": 0})
            if data:
                for k, v in data.items():
                    new_collections[dbname][collname][k] = str(type(v))

    with open("{}/configs/collections.json".format(APPS_PATH), "w") as wf:
        collections = json.dumps(new_collections, indent=4, ensure_ascii=False)
        wf.write(collections)


def init_datas(mdb_sys, mdb_web, mdb_user):
    """
    初始web化数据
    :return:
    """

    for data in INIT_DATAS:

        db = mdb_sys
        if data["db"] == "osr_web":
            db = mdb_web
        elif data["db"] == "osr_user":
            db = mdb_user
        q = {}
        if "condition" in data:
            q = data["condition"]
        if db.dbs[data["coll"]].find_one(q):
            continue
        else:
            print("* [Initialization data] {}".format(data["coll"]))
            db.dbs[data["coll"]].insert_many(data["datas"])

    theme = mdb_sys.db.sys_config.find(
        {"project": "theme", "key": "CURRENT_THEME_NAME"})
    if not theme.count(True):
        # 如果未初始化过
        init_default_datas(mdb_sys, mdb_web, mdb_user)


def init_default_datas(mdb_sys, mdb_web, mdb_user):
    """
    默认主题初始化数据
    """

    init_data = []
    init_file = "{}/themes/osr-style/init_setting.json".format(APPS_PATH)
    if os.path.exists(init_file):
        # 读取数据
        with open(init_file) as rf:
            jsondata = rf.read()
            if jsondata:
                init_data = json.loads(jsondata)

    for data in init_data:

        if mdb_sys.dbs["theme_display_setting"].find_one(
                {"name": data["name"]}):
            continue
        tempdata = deepcopy(data)

        """
        版本更新兼容:找出原来的地方的数据复制, 并删除老数据
        """
        exists_data = mdb_web.db.media.find_one({"name": data["name"]})
        old_id = None
        if exists_data:
            #  如果存在此数据
            tempdata = exists_data
            tempdata["category"] = data["category"]
            old_id = tempdata["_id"]
            del tempdata["_id"]
        else:
            if "text" in tempdata:
                tempdata["text"] = json.dumps(
                    tempdata["text"], ensure_ascii=False)
                tempdata["text_html"] = tempdata["text"]
            elif "text_html" in tempdata:
                tempdata["text_html"] = json.dumps(
                    tempdata["text_html"], ensure_ascii=False)
                tempdata["text"] = tempdata["text_html"]

            other_data = {"link": "",
                          "link_open_new_tab": 0,
                          "link_name": "",
                          "text_imgs": [],
                          "time": time.time(),
                          "user_id": 0,
                          "url": "",
                          "category": "",
                          "title": "title",
                          "text": "",
                          "text_html": ""}

            for k, v in other_data.items():
                if k not in tempdata:
                    tempdata[k] = v

        # 查找是否存在分类
        r = mdb_web.db.category.find_one({"name": tempdata["category"],
                                          "type": "{}_theme".format(tempdata["type"]),
                                          "user_id": 0})
        if r:
            tempdata["category_id"] = str(r["_id"])
        else:
            # 不存在则创建
            r = mdb_web.db.category.insert_one(
                {"name": tempdata["category"],
                 "type": "{}_theme".format(tempdata["type"]),
                 "user_id": 0})
            tempdata["category_id"] = str(r.inserted_id)
        r = mdb_sys.dbs["theme_display_setting"].insert_one(tempdata)
        if r.inserted_id and old_id:
            # 删除旧的数据
            mdb_web.db.media.delete_one({"_id": old_id})
