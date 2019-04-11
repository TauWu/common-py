# -*- coding: utf-8 -*-

from common.request_base import AsyncRequestBase
from common.decode_base import html_to_str
from lxml import etree
import re

class Downloader(object):

    def __init__(self, url_list, **kwargs):
        self._url_list = url_list
        self._headers = None
        if 'headers' in kwargs.keys():
            self._headers = kwargs["headers"]
        req = AsyncRequestBase(self._url_list, self._headers)
        self._content = req.result

    @property
    def yield_from_content(self):
        yield from self._content.items()

class Crawler(object):

    def __init__(self, url, data, html_compile):
        self._idx = re.findall(html_compile, url)[0]
        self._data = data
        self._html = etree.HTML(data)

    def from_xpath(self, xpath):
        datas = list()
        try:
            _data = self._html.xpath(xpath)
            datas = [html_to_str(etree.tostring(data, encoding='utf-8').decode('utf-8')) for data in _data]

        except Exception as e:
            with open(f'temp/{self._idx}.html', 'a') as f:
                f.write(f"{self._data}")
            print(f"error: {e}")
        
        return self._idx, datas

def re_once(content: str, *compiles: re._compile, must: bool=True) -> str:
    for compile in compiles:
        data_list = re.findall(compile, content)
        if len(data_list) > 0: break

    if len(data_list) == 0:
        if must:
            raise ValueError(f"No data matched. [{compiles}]-[{content}]")
        return ""

    return data_list[0]