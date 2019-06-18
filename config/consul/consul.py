# -*- coding: utf-8 -*-

from consulate import Consul
from os import environ
from json import loads

class ConsulConf(object):

    def __init__(self, path="", consul_address=None):

        if consul_address is None:
            consul_address = "127.0.0.1"

        if "CONSUL_ADDR" in environ.keys():
            consul_address = environ["CONSUL_ADDR"]
        
        self._consul = Consul(host=consul_address)
        self._path = path
        self._consul_kv_list = self._consul.kv.items()
        self._consul_value = dict()

    def __load_consul_key__(self, path):
        for kv in self._consul_kv_list:
            if self._path in kv.keys():
                self._consul_value = loads(kv[self._path])

    def __getitem__(self, k):
        self.get(k)

    def __setitem__(self, k, v):
        self.append_kv(k, v)

    def get(self, key):
        for kv in self._consul_kv_list:
            if self._path in kv.keys():
                self._consul_value = loads(kv[self._path])
                break
        
        return(self._consul_value[key] if key in self._consul_value else None)

    def change_path(self, path):
        self._path = path
        self.reload()
        self.__load_consul_key__(path)

    def reload(self):
        self._consul_kv_list = self._consul.kv.items()

    def append_kv(self, k, v):
        self._consul_value = dict(self._consul_value, **{k:v})
        self._consul.kv.set(self._path, self._consul_value)
        self.reload()
    
    def delete_k(self, key):
        self._consul_value.pop(key)
        self._consul.kv.set(self._path, self._consul_value)
        self.reload()
