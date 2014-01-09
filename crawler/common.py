from abc import ABCMeta, abstractmethod
import copy
import socket


class CrawlerConf:
    '''
    Configure a crawler's behaviors.
    '''
    def __init__(self):
        self.max_depth = 0
        
        
class TaskConf:
    '''
    A crawl task configuration object.
    '''
    def __init__(self, domain):
        # process domain or url
        if domain:
            if domain.startswith('https://'):
                raise ValueError('Unsupported HTTPS link!')
            elif domain.startswith('http://'):
                if domain.endswith('/'):
                    self.domain = domain[7:len(domain) - 2]
                else:
                    self.domain = domain[7:len(domain) - 1]
            else:
                self.domain = domain
        else:
            raise ValueError('Invalid domain string!')
        if self.domain:
            self.url = 'http://' + self.domain
            self.ip_addr = self.__get_addr_info(self.domain)
        # initialize default value
        self.max_url_count = -1
        self.priority = 0
        self.max_depth = 0
        self.cross_host_allowed = False
        self.connect_timeout = 3000
        self.socket_timeout = 30000
        
    def __get_addr_info(self, domain):
        ip = None
        try:
            ip = socket.getaddrinfo(domain, 'http')[0][4][0]
        except:
            print('Fail to get ip addr info.')
        return ip
    
    @classmethod
    def clone(cls, domain, task_conf):
        copier = None
        # a domain, or a url
        if task_conf:
            copier = copy.deepcopy(task_conf)
            if domain.startswith('http://'):
                copier.url = domain
            else:
                copier.url = 'http://' + domain
        else:
            copier = TaskConf(domain)
        return copier
    

class Crawler:
    '''
    Abstract crawler, which provides the basic behaviors
    abstraction of a crawler. It depends on the implementation
    about how a crawler works. 
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, crawler_conf, name=None, manager=None):
        self._crawler_conf = crawler_conf
        self._manager = None
        
    @abstractmethod
    def crawl(self, task):
        pass
    
    def get_manager(self):
        return self._manager
    

class HttpEngine:
    '''
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self._initialize()
        
    def _initialize(self):
        self._is_reuseable = True
        self._status_code = 0
        self._resp_headers = {}
        self._binary_data = None
        self._exceptions = []
        
    @abstractmethod
    def fetch(self, url_task):
        pass
    
    @abstractmethod
    def reuse(self):
        pass
    
    def get_status_code(self):
        return self._status_code
    
    def get_resp_header(self, key):
        return self._resp_headers.get(key)
    
    def get_data(self):
        return self._binary_data
    
    def is_reuseable(self):
        return self._is_reuseable
    
        
class Storage:
    '''
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def initialize(self):
        pass
    
    @abstractmethod
    def query_page(self, url):
        pass
    
    @abstractmethod
    def query_all_pages(self):
        pass
    
    @abstractmethod
    def query_all_urls(self):
        pass
    
    @abstractmethod
    def save_page(self, **data):
        pass
    
    @abstractmethod
    def save_url(self, **data):
        pass
    
    @abstractmethod
    def should_crawl(self, url):
        pass
    
    @abstractmethod
    def is_crawled(self, url):
        pass
    
    @abstractmethod
    def close(self):
        pass

    
class CrawlerManager:
    '''
    Manage crawlers
    '''
    __metaclass__ = ABCMeta

    def __init__(self, task_file=None):
        self._http_engine = None
        self._storage = None
        self._crawlers = {}
        self._seed_tasks = []
        
    @abstractmethod
    def create_crawler(self):
        pass
    
    def wait_for(self):
        pass
    
    '''
    Notify the manager the crawler has completed
    the assigned tasks.
    '''
    @abstractmethod
    def notify_complete(self, crawler_name):
        pass
    
    def get_storage(self):
        return self._storage
    
    def get_http_engine(self):
        return self._http_engine
    
