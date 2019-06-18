# -*- coding: utf-8 -*-
from requests import get

class SyncRequestBase(object):

    def __init__(self, url_list, headers=None):
        self._url_dict = {url:None for url in url_list}
        self._url_list = url_list
        self._headers = headers

    @property
    def result(self):
        [self.get_content(url) for url in self._url_list]
        return self._url_dict


    def get_content(self, url):
        data = get(url, headers=self._headers).content
        self._url_dict[url] = data