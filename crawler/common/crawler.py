from abc import ABCMeta, abstractmethod
from socket import socket
from urllib import request
# from http.client import HTTPConnection

from crawler.utils.sequences import UniqIdGenerator
from urllib.error import HTTPError


class Crawler:
    '''
    Abstract crawler, which provides the basic behaviors
    abstraction of a crawler. It depends on the implementation
    about how a crawler works. 
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, conf=None):
        self.conf = conf
        
    def setConf(self, conf):
        self.conf = conf
    
    @abstractmethod
    def crawl(self, task):
        pass
    
    @abstractmethod
    def getResult(self):
        pass
    
class CrawlResult:
    '''
    The result of a crawler fetching a page.
    '''
    def __init__(self, urlTask):
        self.urlTask = urlTask
        self.data = None
        self.statusCode = None
        

class DefaultCrawler(Crawler):
    '''
    Default crawler implementation class.
    References:
    1. http://en.wikipedia.org/wiki/List_of_HTTP_header_fields
    '''

    reqHeaders = {
        'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
    }
    
    def __init__(self, conf, name=None):
        super(DefaultCrawler, self).__init__(conf)
        self.name = name
        if name is None:
            name  = str(UniqIdGenerator.nextId(__name__))
            
    def crawl(self, seedTask):
        url = seedTask.getUrl()
        #connection = HTTPConnection()
        socketTimeout = socket.socket._GLOBAL_DEFAULT_TIMEOUT
        if seedTask.taskConf is not None:
            socketTimeout = seedTask.taskConf.socketTimeout
        req = request.Request(url, headers=DefaultCrawler.reqHeaders)
        
        result = CrawlResult()
        try:
            u = request.urlopen(req, socketTimeout)
        except HTTPError as e:
            result.statusCode = e.code
        else:
            response = u.read()
            if response is not None:
                result.data = response
        

  
