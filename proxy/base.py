from abc import ABCMeta, abstractclassmethod

class ProxyBase(object, metaclass=ABCMeta):

    @abstractclassmethod
    def init_proxy(self):
        ''' create_proxy

        '''

    @abstractclassmethod
    def proxy_request(self, url: str, method: str, **kwargs):
        '''get_proxy

        '''
