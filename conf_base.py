# -*- coding: utf-8 -*-
# Read conf by files or consul.

from configparser import ConfigParser
from consulate import Consul
from os import environ
from json import loads

class FileConf(object):

    def __init__(self, path="conf/base.cfg", section="base"):
        self._path = path
        self._section = section
        self._conf = ConfigParser()
        self._conf.read(self._path)

    def add_section(self, section_name):
        self._conf.add_section(section_name)
        self.use_section(section_name)

    def use_section(self, section_name):
        self._section = section_name

    def set_kv(self, k, v):
        self._conf.set(self._section, k, str(v))
        self.save()

    def save(self):
        self._conf.write(open(self._path, 'w'))

    def __getitem__(self, k):
        return self.get(k)

    def get(self, k):
        return self._conf[self._section][k]

    @property
    def all(self):
        return {k:self.get(k) for k in self._conf[self._section]}

    @staticmethod
    def read_section_conf(conf_path, section, *args, **kwargs):

        file_conf = FileConf(path=conf_path, section=section)

        if "all" in kwargs.keys() and kwargs["all"]:
            return file_conf.all

        if len(args) == 1:
            return file_conf.get(args[0])

        return {k: file_conf.get(k) for k in args}

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
