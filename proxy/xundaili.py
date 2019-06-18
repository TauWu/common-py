# -*- coding: utf-8 -*-

from time import time
from hashlib import md5
from requests import get, post
from common.python.consul import ConsulConf
from common.python.file import FileConf

class XunDaiLiProxy(ProxyBase):

    def __init__(self):
        self.init_proxy()
        self.headers = {"Proxy-Authorization":self._auth}
        self.cookies = dict()
        self.data = dict()

    def init_proxy(self):
        try:
            cfg = ConsulConf("proxy/xundaili", "127.0.0.1")
        except Exception:
            cfg = FileConf("conf/proxy", "xundaili")

        self._timestamp = str(int(time()))

        str_encode = f'orderno={cfg.get("orderno")},secret={cfg.get("secret")},timestamp={self._timestamp}'.encode()
        str_decode = md5(str_encode).hexdigest().upper()
        self._auth = f'sign={str_decode}&orderno={cfg.get("orderno")}&timestamp={self._timestamp}'
        self._proxy = dict(http="http://%s"%(cfg.get("host")), https="https://%s"%(cfg.get("host")))

    def add_headers(self, **kwargs):
        self.headers = dict(self.headers, **kwargs)

    async def async_proxy_request(self, url: str, method: str, session):
        
        if method == "GET":
            async with session.get(url, headers=self.headers, cookies=self.cookies, allow_redirects=False, verify_ssl=False, proxy=self._proxy["http"]) as response:
                    return await response.text()

        elif method == "POST":
            async with session.post(url) as response:
                    return await response.text()

        else:
            raise ValueError("bad method")

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
