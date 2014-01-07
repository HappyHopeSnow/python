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
    
    def __init__(self, crawler_conf=None):
        self.crawler_conf = crawler_conf
        
    @abstractmethod
    def crawl(self, task):
        pass
    

class HttpEngine:
    '''
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def fetch(self, url_task):
        pass
    
    @abstractmethod
    def get_status_code(self):
        pass
    
    @abstractmethod
    def get_resp_header(self, key):
        pass
    
    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def reuse(self):
        pass
    
    @abstractmethod
    def is_reuseable(self):
        pass
    
        


