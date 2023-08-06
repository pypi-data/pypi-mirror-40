#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hash_algorithm


def add_in_dict_list(mapping, key, val):
    table = mapping.get(key)
    if not table:
        mapping[key] = [val]
    else:
        table.append(val)


class RedisShardingClient:
    """
    weight配置在python端和java端必须保持一致
    demo:
    link:
    """

    def __init__(self, sentinel, masters):
        self.__sentinel = sentinel
        self.__masters = masters
        self.__common_stack = []
        self.__sharding_nodes = {}
        self.__nodes_dict = {}
        for node in masters:
            weight = node.connection_pool.connection_kwargs.get('weight', 1)
            self.__sharding_nodes[node.connection_pool.service_name] = (weight, node)
        self.__shared_pool = {}
        self.__pipes = {}
        for master_name in self.__sharding_nodes.keys():
            weight = int(self.__sharding_nodes.get(master_name)[0])
            for n in range(0, 160 * weight):
                shared_info = hash_algorithm.get_hash('%s*%s%s' % (master_name, weight, n))
                self.__shared_pool[shared_info] = master_name
        self.__router_table = self.__shared_pool.keys()
        self.__router_table.sort()

    def __get_master_by_commands(self, keys):
        master_keys_mapping = {}
        for k in keys:
            hash_val = hash_algorithm.get_hash(k[0])
            in_scope = False
            for slot in self.__router_table:
                if slot >= hash_val:
                    add_in_dict_list(master_keys_mapping, self.__shared_pool[slot], k)
                    in_scope = True
                    break
            if not in_scope:
                slot = self.__router_table[0]
                add_in_dict_list(master_keys_mapping, self.__shared_pool[slot], k)
        return master_keys_mapping

    def set(self, key, value):
        self.__common_stack.append((key, value, 'set'))

    def pipeline(self):
        self.__common_stack = []
        return self

    def expire(self, name, time):
        self.__common_stack.append((name, time, 'expire'))

    def __get_pipe(self, master):
        pipe = self.__pipes.get(master)
        if not pipe:
            master_client = self.__sharding_nodes.get(master)[1]
            pipe = master_client.pipeline()
            self.__pipes[master] = pipe
        return pipe

    def execute(self):
        master_commands_mapping = self.__get_master_by_commands(self.__common_stack)
        for master in master_commands_mapping.keys():
            pipe = self.__get_pipe(master)
            commands = master_commands_mapping.get(master)
            for command in commands:
                if command[2] == 'set':
                    pipe.set(command[0], command[1])
                else:
                    pipe.expire(command[0], command[1])
            pipe.execute()
        self.__common_stack = []

# shared_masters = {'master-1': 1, 'master-2': 1, 'master-3': 1}

# print router_table
#
# test_keys = []
# for i in range(0, 100):
#     print get_master_by_keys(["sdfdasfc_city_id_1231fdf_rider_id_%d" % i])
