# -*- coding: utf-8 -*
from common.python.request import AsyncRequestBase

class Downloader(object):

    def __init__(self, url_list, proxy=None,**kwargs):
        self._url_list = url_list
        self._headers = None
        if 'headers' in kwargs.keys():
            self._headers = kwargs["headers"]
        req = AsyncRequestBase(self._url_list, self._headers, proxy)
        self._content = req.result

    @property
    def yield_from_content(self):
        yield from self._content.items()