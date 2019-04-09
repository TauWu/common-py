# -*- coding: utf-8 -*-

from aiohttp import ClientSession, TCPConnector
from requests import get
from asyncio import get_event_loop

class AsyncRequestBase(object):

    def __init__(self, url_list, headers=None):

        self._url_dict = {url:None for url in url_list}
        self._url_list = url_list
        self.__loop = get_event_loop()
        self._aiohttp_connector = TCPConnector(limit=100) # Limit for TCPConnector.
        self._headers = headers

    @property
    def result(self):
        self.__loop.run_until_complete(
            self.get_content()
        )
        return self._url_dict

    async def get_content(self):
        async with ClientSession(connector=self._aiohttp_connector, headers=self._headers) as session:
            for url in self._url_list:
                async with session.get(url=url) as resp:
                    data = await resp.text()
                self._url_dict[url] = data

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

if __name__ == "__main__":
    # Test code
    import time
    headers = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    tm_start = time.time()
    url_list = [ "http://product.dangdang.com/%d.html"%idx for idx in range(26516153, 26516155) ]

    req = AsyncRequestBase(url_list, headers=headers)
    print(req.result)
    tm_end_async = time.time()


    req = SyncRequestBase(url_list, headers=headers)
    print(req.result)
    tm_end_sync = time.time()

    print(f"async: {tm_end_async-tm_start}s sync:{tm_end_sync-tm_end_async}s")
