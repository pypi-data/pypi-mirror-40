# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zredis.py
   Author :       Zhang Fan
   date：         2019/1/10
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import json

import redis
from zretry import retry

_retry_func_list = []


def _except_retry(func):
    _retry_func_list.append(func.__name__)
    return func


class redis_inst():
    def __init__(self, host: str or list, port=6379, cluster=False, collname='test', password=None,
                 decode_responses=True,
                 retry_interval=1, max_attempt_count=5,
                 **kw):
        '''
        创建一个redis客户端
        :param host: 单点服务器ip, 集群设置为list类型, 格式[{"host": "IP地址", "port": "端口"}, {"host": "IP地址", "port": "端口"]
        :param port: 单点服务器端口
        :param cluster: 是否为集群
        :param collname: 文档名
        :param password: 密码
        :param decode_responses: 是否解码
        :param retry_interval: 尝试等待时间
        :param max_attempt_count: 最大尝试次数
        :param kw: 其他参数
        '''
        if cluster:
            from rediscluster import StrictRedisCluster
            self._conn = StrictRedisCluster(
                startup_nodes=eval(host) if isinstance(host, str) else host,
                password=password, decode_responses=decode_responses, **kw)
        else:
            rpool = redis.ConnectionPool(host=host, port=port, password=password,
                                         decode_responses=decode_responses, **kw)
            self._conn = redis.Redis(connection_pool=rpool)
        self.collname = collname

        for retry_func_name in _retry_func_list:
            func = getattr(self, retry_func_name)
            decorator = retry(interval=retry_interval, max_attempt_count=max_attempt_count)(func)
            setattr(self, retry_func_name, decorator)

    # region 其他操作
    def change_coll(self, collname):
        self.collname = collname

    @_except_retry
    def collnames(self):
        return [name for name in self._conn.scan_iter()]

    @_except_retry
    def collnames_iter(self):
        return self._conn.scan_iter()

    @_except_retry
    def save_db(self, bgsave=False):
        # 返回是否成功
        if bgsave:
            return self._conn.bgsave()
        return self._conn.save()

    @_except_retry
    def delete_coll(self, *collname):
        return self._conn.delete(*collname)

    @_except_retry
    def rename(self, newname, collname=None):
        return self._conn.rename(collname or self.collname, newname)

    @_except_retry
    def has_collname(self, collname):
        return self._conn.exists(collname)

    @_except_retry
    def type_collname(self, collname):
        # 返回文档类型("hash","list","set","zset","string","none")
        return self._conn.type(collname)

    @_except_retry
    def collnames_count(self):
        # 统计有多少个文档, 如果是集群则返回一个dict 如 {'xxx.xxx.xxx.xxx:1234': 100}
        return self._conn.dbsize()

    # endregion

    # region 列表操作
    @_except_retry
    def list_push(self, text: str, front=True):
        # 放入一个字符串, 返回队列总数
        if front:
            return self._conn.lpush(self.collname, text)
        else:
            return self._conn.rpush(self.collname, text)

    @_except_retry
    def list_pop(self, front=True):
        # 无数据时返回None
        if front:
            return self._conn.lpop(self.collname)
        else:
            return self._conn.rpop(self.collname)

    @_except_retry
    def list_count(self, collname=None):
        return self._conn.llen(collname or self.collname)

    def list_push_dict(self, item: dict, front=True, encode_chinese=True):
        # 返回队列总数
        text = json.dumps(item, ensure_ascii=encode_chinese)
        return self.list_push(text, front=front)

    def list_pop_dict(self, front=True, default=None):
        text = self.list_pop(front=front)
        if not text is None:
            return json.loads(text)
        return default

    @_except_retry
    def list_get_datas(self, start=0, end=-1):
        # 列表切片, 和python不同的是, 包含end位置的元素
        return self._conn.lrange(self.collname, start, end)

    @_except_retry
    def list_iter(self):
        range_count = 10
        count = self.list_count()
        index = 0
        while index < count:
            datas = self.list_get_datas(start=index, end=index + range_count - 1)
            for data in datas:
                yield data

            index += len(datas)
            if not datas or index >= count:
                return

    # endregion

    # region 集合操作
    @_except_retry
    def set_add(self, data):
        # 返回是否成功
        return self._conn.sadd(self.collname, data) == 1

    @_except_retry
    def set_add_values(self, *data):
        # 返回添加成功的数量
        return self._conn.sadd(self.collname, *data)

    @_except_retry
    def set_remove(self, *data):
        # 删除多个值
        return self._conn.srem(self.collname, *data)

    @_except_retry
    def set_count(self, collname=None):
        return self._conn.scard(collname or self.collname)

    @_except_retry
    def set_has(self, value):
        # 是否存在某个值
        return self._conn.sismember(self.collname, value)

    @_except_retry
    def set_get_datas(self):
        # 返回一个set, 包含redis中该set的所有数据
        return self._conn.smembers(self.collname)

    @_except_retry
    def set_iter(self):
        # 迭代返回一个set中所有的数据
        return self._conn.sscan_iter(self.collname)

    # endregion

    # region 哈希操作
    @_except_retry
    def hash_set(self, key, value):
        # 设置数据, 返回0表示修改,返回1表示创建
        return self._conn.hset(self.collname, key, value)

    @_except_retry
    def hash_set_values(self, mapping: dict):
        # 设置多个数据, 返回是否成功
        return self._conn.hmset(self.collname, mapping)

    @_except_retry
    def hash_get(self, key):
        # 获取一个key的值, 失败返回None
        return self._conn.hget(self.collname, key)

    @_except_retry
    def hash_remove(self, *keys):
        # 删除多个键, 返回实际删除数量
        return self._conn.hdel(self.collname, *keys)

    @_except_retry
    def hash_incrby(self, key, amount=1):
        # 自增, 返回自增后的值
        return self._conn.hincrby(self.collname, key, amount=amount)

    @_except_retry
    def hash_count(self, collname=None):
        return self._conn.hlen(collname or self.collname)

    @_except_retry
    def hash_has(self, key):
        # 是否存在某个键
        return self._conn.hexists(self.collname, key)

    @_except_retry
    def hash_keys(self):
        # 返回字典中所有的key
        return self._conn.hkeys(self.collname)

    @_except_retry
    def hash_get_datas(self):
        # 返回一个字典, 包含redis中该hash中的所有数据
        return self._conn.hgetall(self.collname)

    @_except_retry
    def hash_iter(self):
        # 迭代返回一个hash中所有的数据, 每次返回的是一个元组(键, 值)
        return self._conn.hscan_iter(self.collname)

    # endregion
