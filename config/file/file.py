
# -*- coding: utf-8 -*-
from configparser import ConfigParser

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
