# -*- coding: utf-8 -*-

from aiohttp import ClientSession, TCPConnector
from aiohttp.client_exceptions import ServerDisconnectedError, ClientConnectionError
from requests import get
from asyncio import get_event_loop, gather, ensure_future, wait, sleep

class AsyncRequestBase(object):

    def __init__(self, url_list, headers=None, proxy=None):

        self._url_dict = {url:None for url in url_list}
        self._url_list = url_list
        self.__loop = get_event_loop()
        self._aiohttp_connector = TCPConnector(limit=1000) # Limit for TCPConnector.
        self._headers = headers
        self._proxy = proxy

    @property
    def result(self):
        try:
            tasks = [ensure_future(self.get_content(url)) for url in self._url_list]
            self.__loop.run_until_complete(
                gather(*tasks)
            )
        except ServerDisconnectedError:
            print("Request success")

        return self._url_dict

    async def get_content(self, url):
        async with ClientSession(connector=self._aiohttp_connector, headers=self._headers) as session:
            if self._proxy is None:
                async with session.get(url=url, timeout=10) as resp:
                    data = await resp.text()
            else:
                async with session.get(url=url) as resp:
                    data = await self._proxy.async_proxy_request(url, "GET", session)
            self._url_dict[url] = data
            return

    @property
    def postresult(self):
        try:
            tasks = [self.get_post_content(url[0], url[1]) for url in self._url_list]
            self.__loop.run_until_complete(
                gather(*tasks)
            )
        except (ClientConnectionError, ServerDisconnectedError) as e:
            print("Request timeout =>", e)

        return self._url_dict

    async def get_post_content(self, url, payload):
        async with ClientSession(connector=self._aiohttp_connector, headers=self._headers) as session:
            await self.postfetch(session, url, payload)
            await sleep(1)

    async def postfetch(self, session, url, payload):
        async with session.post(url=url, data=payload) as resp:
            self._url_dict[(url, payload)] = await resp.text()


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
