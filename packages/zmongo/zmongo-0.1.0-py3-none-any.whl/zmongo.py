# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zmongo.py
   Author :       Zhang Fan
   date：         2019/1/10
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from pymongo import MongoClient
from zretry import retry

_retry_func_list = []


def _except_retry(func):
    _retry_func_list.append(func.__name__)
    return func


class mongo_inst():
    def __init__(self, host: str, port: int, db: str = 'test', collname=None, user=None, password=None,
                 retry_interval=1, max_attempt_count=5,
                 **kw):
        '''
        创建一个mongo客户端
        :param host: ip地址
        :param port: 端口
        :param db: 数据库
        :param collname: 文档名
        :param user: 用户名
        :param password: 密码
        :param retry_interval: 尝试等待时间
        :param max_attempt_count: 最大尝试次数
        :param kw: 其他参数
        '''
        self._conn = MongoClient(host=host, port=port, **kw)
        if user and password:
            self._conn[db].authenticate(user, password)
        self.change_db(db, collname)

        for retry_func_name in _retry_func_list:
            func = getattr(self, retry_func_name)
            decorator = retry(interval=retry_interval, max_attempt_count=max_attempt_count)(func)
            setattr(self, retry_func_name, decorator)

    def change_db(self, db, collname=None):
        self.db_name = db
        self.collname = collname
        self.coll = self._conn[db][collname] if collname else None

    def change_coll(self, collname):
        self.collname = collname
        self.coll = self._conn[self.db_name][collname]

    @_except_retry
    def save(self, item):
        # 保存数据,成功返回_id,失败报错
        return self.coll.insert(item)

    def all_data(self, collname=None, skip_count=0):
        assert isinstance(skip_count, int) and skip_count >= 0, 'skip必须是整数且不能小于0'

        if collname:
            self.change_coll(collname)

        datas = self.coll.find()

        if skip_count:
            datas.skip(skip_count)

        return datas

    def find(self, *args, **kw):
        return self.coll.find(*args, **kw)

    def find_id(self, _id):
        return self.coll.find({'_id': _id})

    def find_fields(self, *fields):
        return self.coll.find({}, {field: True for field in fields})

    def del_id(self, _id):
        return self.coll.delete_one({'_id': _id})
