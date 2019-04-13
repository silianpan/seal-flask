# -*-coding:utf-8-*-
import time
from flask import request
from apps.app import mdb_web, cache
from apps.core.utils.get_config import get_config
# from apps.utils.async.async import async_process
from apps.utils.format.obj_format import json_to_pyseq, str_to_num

__author__ = 'Allen Woo'


def get_tags():
    """
    根据条件获取post tags
    :return:
    """
    last_days = str_to_num(request.argget.all('last_days', 360))
    user_id = request.argget.all('user_id')
    tlimit = str_to_num(request.argget.all('limit', 20))
    tsort = json_to_pyseq(request.argget.all('sort', [{"tag_cnt": -1},
                                                      {"like": -1},
                                                      {"comment_num": -1}]))
    # sort
    sort = {}
    for s in tsort:
        sort = dict(sort, **s)

    # 查看是否存在缓存
    cache_key = cache.get_autokey(
        fun="_get_tags",
        key_base64=False,
        db_type="redis",
        user_id=user_id,
        last_days=last_days,
        tlimit=tlimit,
        sort=sort)
    data = cache.get(key=cache_key, db_type="redis")
    if data != cache.cache_none:
        return data
    else:
        # 存在, 调用生成缓存程序生成新缓存
        async_get_tags(user_id, last_days, tlimit, sort)

        # 然后返回最后一次的长期缓存
        data = cache.get(key="LAST_POST_TAGS_CACHE", db_type="mongodb")
        return data


# @async_process
async def async_get_tags(user_id, last_days, tlimit, sort):
    """
    开子进程统计tag结果
    :param last_days:
    :param tlimit:
    :param sort:
    :return:
    """
    mdb_web.init_app(reinit=True)
    _get_tags(user_id=user_id, last_days=last_days, tlimit=tlimit, sort=sort)


@cache.cached(timeout=3600 * 12, key_base64=False, db_type="redis")
def _get_tags(user_id, last_days, tlimit, sort):
    ut = time.time()
    s_time = ut - last_days * 86400 - ut % 86400
    query_conditions = {
        "issue_time": {
            "$gt": s_time},
        "issued": 1,
        "is_delete": 0,
        "audit_score": {
            "$lt": get_config(
                "content_inspection",
                "ALLEGED_ILLEGAL_SCORE")}}
    if user_id:
        query_conditions["user_id"] = user_id

    # 查询出部分pv量大的文章
    sort["cnt"] = -1
    r = mdb_web.db.post.aggregate([
        {"$match": query_conditions},
        {"$unwind": "$tags"},
        {
            "$group": {"_id": "$tags",
                       "tag_cnt": {"$sum": 1},
                       "like": {"$sum": "$like"},
                       "comment_num": {"$sum": "$comment_num"}}
        },
        {"$sort": sort},
        {"$limit": tlimit},
    ], allowDiskUse=True)
    data = {"tags": []}
    for result in r:
        tr = {
            "tag": result["_id"],
            "like": result["like"],
            "comment_num": result["comment_num"]
        }
        data["tags"].append(tr)

    # 保留一份长期缓存
    cache.set(
        key="LAST_POST_TAGS_CACHE",
        value=data,
        ex=3600 * 24 * 7,
        db_type="mongodb")
    return data
