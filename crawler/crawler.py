# -*- coding: utf-8 -*-
from common.python.decode import html_to_str
from lxml import etree
import re

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

def re_cycle(content: str, *compiles: re._compile, must: bool=True) -> list:
    for compile in compiles:
        data_list = re.findall(compile, content)
        if len(data_list) > 0: break

    if len(data_list) == 0:
        if must:
            raise ValueError(f"No data matched. [{compiles}]-[{content}]")
        return []
    
    return data_list
