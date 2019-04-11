# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractclassmethod
from time import time
from hashlib import md5
from requests import get, post
from common.conf_base import ConsulConf, FileConf

class ProxyBase(object, metaclass=ABCMeta):

    @abstractclassmethod
    def init_proxy(self):
        ''' create_proxy

        '''

    @abstractclassmethod
    def proxy_request(self, url: str, method: str, **kwargs):
        '''get_proxy

        '''
    
class XunDaiLiProxy(ProxyBase):

    def __init__(self):
        self.init_proxy()
        self.headers = dict()
        self.cookies = dict()
        self.data = dict()

    def init_proxy(self):
        try:
            cfg = ConsulConf("proxy/xundaili", "127.0.0.1")
        except Exception:
            cfg = FileConf("conf/proxy", "xundaili")
        self._timestamp = str(int(time()))

        str_encode = f'orderno={cfg["orderno"]},secret={cfg["secret"]},timestamp={self._timestamp}'.encode()
        str_decode = md5(str_encode).hexdigest().upper()
        self._auth = f'sign={str_decode}&orderno={cfg["orderno"]}&timestamp={self._timestamp}'
        self._proxy = dict(http=f"http://{cfg[host]}", https=f"https://{cfg[host]}")

    def add_headers(self, **kwargs):
        self.headers = dict(self.headers, **kwargs)

    def proxy_request(self, url: str, method: str, **kwargs):

        idx = 0
        content = None

        while True:
            idx +=  1

            try:
                if method == "GET":
                    content = get(url, headers=self.headers, cookies=self.cookies, proxies=self._proxy, allow_redirects=False, timeout=20, verify=False, data=self.data).content

                elif method == "POST":
                    content = post(url, headers=self.headers, cookies=self.cookies, proxies=self._proxy, allow_redirects=False, timeout=20, verify=False, data=self.data).content
            
            except Exception as e:
                if idx <= 10:
                    continue
                raise(e)

            if str(content).find("The number of requests exceeds the limit") != -1:
                print("Exceed the limit, STOP!!!")
                break

            if str(content).find("Bad Gateway") != -1 or str(content).find("The requested URL could not be retrieved") != -1:
                print("Get bad gateway, continue ...")
                if idx > 10:
                    break
                continue

            return content
