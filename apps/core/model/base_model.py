#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-14 14:09
# @Author  : liupan
# @Site    : 
# @File    : base_model.py
# @Software: PyCharm

from flask import json
from sqlalchemy.orm.attributes import QueryableAttribute
from apps.core.db.mysql import db
from sqlalchemy.exc import IntegrityError, OperationalError


class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs):
        kwargs["_force"] = True
        self.from_dict(**kwargs)

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'crt_time', 'upd_time', 'crt_user', 'upd_user', 'del_flag', 'version'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                            self.__mapper__.relationships[key].query_class is not None
                            or self.__mapper__.relationships[key].instrument_class
                            is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide), _path=("%s.%s" % (_path, key.lower()))
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data

    def from_dict(self, **kwargs):
        """Update this model with a dictionary."""

        _force = kwargs.pop("_force", False)

        readonly = self._readonly_fields if hasattr(self, "_readonly_fields") else []
        if hasattr(self, "_hidden_fields"):
            readonly += self._hidden_fields

        readonly += ['id', 'crt_time', 'upd_time', 'crt_user', 'upd_user', 'del_flag', 'version']

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        changes = {}

        for key in columns:
            if key.startswith("_"):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists:
                val = getattr(self, key)
                if val != kwargs[key]:
                    changes[key] = {"old": val, "new": kwargs[key]}
                    setattr(self, key, kwargs[key])

        for rel in relationships:
            if key.startswith("_"):
                continue
            allowed = True if _force or rel not in readonly else False
            exists = True if rel in kwargs else False
            if allowed and exists:
                is_list = self.__mapper__.relationships[rel].uselist
                if is_list:
                    valid_ids = []
                    query = getattr(self, rel)
                    cls = self.__mapper__.relationships[rel].argument()
                    for item in kwargs[rel]:
                        if (
                                "id" in item
                                and query.filter_by(id=item["id"]).limit(1).count() == 1
                        ):
                            obj = cls.query.filter_by(id=item["id"]).first()
                            col_changes = obj.from_dict(**item)
                            if col_changes:
                                col_changes["id"] = str(item["id"])
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(item["id"]))
                        else:
                            col = cls()
                            col_changes = col.from_dict(**item)
                            query.append(col)
                            db.session.flush()
                            if col_changes:
                                col_changes["id"] = str(col.id)
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(col.id))

                    # delete rows from relationship that were not in kwargs[rel]
                    for item in query.filter(not_(cls.id.in_(valid_ids))).all():
                        col_changes = {"id": str(item.id), "deleted": True}
                        if rel in changes:
                            changes[rel].append(col_changes)
                        else:
                            changes.update({rel: [col_changes]})
                        db.session.delete(item)

                else:
                    val = getattr(self, rel)
                    if self.__mapper__.relationships[rel].query_class is not None:
                        if val is not None:
                            col_changes = val.from_dict(**kwargs[rel])
                            if col_changes:
                                changes.update({rel: col_changes})
                    else:
                        if val != kwargs[rel]:
                            setattr(self, rel, kwargs[rel])
                            changes[rel] = {"old": val, "new": kwargs[rel]}

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists and getattr(self.__class__, key).fset is not None:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    val = val.to_dict()
                changes[key] = {"old": val, "new": kwargs[key]}
                setattr(self, key, kwargs[key])

        return changes

    @classmethod
    def _get_or_create(
            cls,
            _session=None,
            _filters=None,
            _defaults={},
            _retry_count=0,
            _max_retries=3,
            **kwargs
    ):
        if not _session:
            _session = db.session
        query = _session.query(cls)
        if _filters is not None:
            query = query.filter(*_filters)
        if len(kwargs) > 0:
            query = query.filter_by(**kwargs)

        instance = query.first()
        if instance is not None:
            return instance, False

        _session.begin_nested()
        try:
            kwargs.update(_defaults)
            instance = cls(**kwargs)
            _session.add(instance)
            _session.commit()
            return instance, True

        except IntegrityError:
            _session.rollback()
            instance = query.first()
            if instance is None:
                raise
            return instance, False

        except OperationalError:
            _session.rollback()
            instance = query.first()
            if instance is None:
                if _retry_count < _max_retries:
                    return cls._get_or_create(
                        _filters=_filters,
                        _defaults=_defaults,
                        _retry_count=_retry_count + 1,
                        _max_retries=_max_retries,
                        **kwargs
                    )
                raise
            return instance, False

    @classmethod
    def get_or_create(cls, **kwargs):
        return cls._get_or_create(**kwargs)[0]
