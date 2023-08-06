#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis.sentinel import Sentinel

from src.redis_sharding_client import RedisShardingClient
import time


def bulk_write(batch):
    sentinel = Sentinel([('127.0.0.1', 26001), ('127.0.0.2', 26001), ('127.0.0.3', 26001)],
                        socket_timeout=3)
    master1 = sentinel.master_for('master-0', socket_timeout=10, password='123123')
    master2 = sentinel.master_for('master-1', socket_timeout=10, password='123123')
    master3 = sentinel.master_for('master-3', socket_timeout=10, password='123123')
    sharding_client = RedisShardingClient(sentinel, [master1, master3, master2])
    pipe = sharding_client.pipeline()
    expire = 20
    index = 0
    for record in batch:
        key = record[0]
        value = record[1]
        pipe.set(key, value)
        pipe.expire(key, expire)
        if index >= 2000:
            pipe.execute()
            time.sleep(0.1)
            index = 0
    pipe.execute()


if __name__ == '__main__':
    data = []
    for i in range(0, 200):
        k = 'realtime_compute_c_id_2322_r_id_%d' % i
        v = 'value%d' % i
        data.append((k, v))
    bulk_write(data)
