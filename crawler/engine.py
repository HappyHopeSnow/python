from abc import ABCMeta, abstractmethod
import copy
import re
import socket
from urllib.error import HTTPError
import urllib.request

from crawler.utils.sequences import UniqIdGenerator


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
    

class UrlTask:
    '''
    A task encapsulates crawler related url resources before starting
    to crawl pages represented by a url.
    '''
    def __init__(self, task_conf):
        self.task_conf = task_conf
        self.url = task_conf.url
        self.crawl_result = CrawlResult(self.url)
        self.depth = 0
        
    def __str__(self):
        return 'url = ' + self.url
        
    
class TaskFactory:
    '''
    Build url tasks from a given file.
    '''
    @classmethod
    def build_seeds(cls, task_file):
        url_tasks = []
        try:
            f = open(task_file, 'r')
        except:
            raise IOError('Error to open file: ' + task_file)
        for line in f:
            if not line.strip().startswith('#'):
                a = line.strip().split(',')
                if len(a) == 7:
                    # domain or url
                    domain = a[0].lower().strip()
                    if len(domain) > 0:
                        task_conf = TaskConf(domain)
                    # max url count
                    max_url_count = a[1].strip()
                    if len(max_url_count) > 0:
                        task_conf.max_url_count = int(max_url_count)
                    # priority
                    priority = a[2].strip()
                    if len(priority) > 0:
                        task_conf.priority = int(priority)
                    # max depth
                    max_depth = a[3].strip()
                    if len(max_depth) > 0:
                        task_conf.max_depth = int(max_depth)
                    # cross host allowed
                    cross_host_allowed = a[4].lower().strip()
                    if len(cross_host_allowed) > 0:
                        if cross_host_allowed == 'true':
                            task_conf.cross_host_allowed = True
                        else:
                            task_conf.cross_host_allowed = False
                    # connection timeout
                    connect_timeout = a[5].lower().strip()
                    if len(connect_timeout) > 0:
                        task_conf.connect_timeout = int(connect_timeout)
                    # socket timeout
                    socket_timeout = a[6].lower().strip()
                    if len(socket_timeout) > 0:
                        task_conf.socket_timeout = int(socket_timeout)
                        
                    url_task = UrlTask(task_conf)
                    url_tasks.append(url_task)
        f.close()
        return url_tasks
    
    @classmethod
    def build_url_tasks(cls, url_task):
        url_tasks = []
        if not url_task and not url_task.crawl_result:
            return url_tasks
        if url_task.depth <= url_task.task_conf.max_depth:
            depth = url_task.depth + 1
            # extract url from the page source data
            urls = ResultParser.extract_urls(url_task.crawl_result)
            for url in urls:
                print('Crawl page: url = ' + url)
                conf = TaskConf.clone(url, url_task.task_conf)
                task = UrlTask(conf)
                task.depth = depth
                url_tasks.append(task)
        return url_tasks
    

class ResultParser:
    
    @classmethod
    def extract_urls(cls, crawl_result):
        urls = []
        if crawl_result.status_code == 200:
            string_data = cls.__get_string_data(crawl_result)
            if len(string_data) > 0:
                all_urls = re.findall(r"<a.*?href=\s*[\"']*([^\"']+).*?<\/a>", string_data, re.I)
                for url in all_urls:
                    if url and cls.__is_valid_url(url.strip()):
                        urls.append(url)
        return urls
    
    @classmethod
    def __is_valid_url(cls, url): 
        is_valid = False
        if url:
            is_valid = url.startswith('http://') 
        return is_valid
        #and url.startswith('#') and url.startswith('/')
    
    @classmethod     
    def extract_anchors(cls, crawl_result):
        anchors = []
        if crawl_result.starus_code == 200:
            string_data = cls.__get_string_data(crawl_result)
            if len(string_data) > 0:
                anchors = re.findall(r"<a.*?href=.*?<\/a>", string_data, re.I)
        return anchors
    
    @classmethod
    def __get_string_data(cls, crawl_result):
        string_data = ''
        data = crawl_result.binary_data
        if data:
            string_data = data.decode(crawl_result.charset)
        return string_data
   

class HttpEngine:
    '''
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def fetch(self, url_task):
        pass


class DefaultHttpEngine(HttpEngine):
    '''
    '''
    reqHeaders = {
        'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
    }
    
    def __init__(self):
        pass
    
    def fetch(self, url_task):
        url = url_task.url
        result = CrawlResult(url)
        try:
            response = urllib.request.urlopen(url)
        except HTTPError as e:
            result.status_code = e.code
            result.exceptions.append(e)
        except BaseException as e:
            result.exceptions.append(e)
        else:
            result.status_code = response.status
            for h in response.headers:
                result.response_headers[h] = response.headers[h]
            data = response.read()
            if data:
                result.binary_data = data
        return result
    
class CrawlerConf:
    '''
    Configure a crawler's behaviors.
    '''
    def __init__(self):
        self.engine = DefaultHttpEngine()
        self.max_depth = 0
        

# from http.client import HTTPConnection
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

    
class CrawlResult:
    '''
    The result of a crawler fetching a page.
    '''
    def __init__(self, url):
        self.url = url
        self.binary_data = None
        self.string_data = None
        self.status_code = None
        self.charset = 'UTF-8'
        self.urls = []
        self.response_headers = {}
        self.exceptions = []
        
    def __str__(self):
        return 'url = ' + self.url + ', charset=' + self.charset
        

class DefaultCrawler(Crawler):
    '''
    Default crawler implementation class.
    References:
    1. http://en.wikipedia.org/wiki/List_of_HTTP_header_fields
    '''
    def __init__(self, conf, name=None):
        super(DefaultCrawler, self).__init__(conf)
        self.name = name
        if not name:
            seed = self.__class__.__name__
            name  = str(UniqIdGenerator.next_id(seed))
        print('Create crawler#' + name)
            
    def crawl(self, url_task):
        # crawl a url task built from the seed file
        task = url_task
        if task:
            # compute max depth of crawling pages
            max_depth = self.crawler_conf.max_depth
            if task.task_conf.max_depth:
                # override default max depth configuration
                max_depth = task.task_conf.max_depth
            depth = 0
            while depth <= max_depth:
                result = self.crawler_conf.engine.fetch(task)
                # save result
                # TODO
                if result:
                    task.crawl_result = result
                    if depth <= max_depth - 1:
                        url_tasks = TaskFactory.build_url_tasks(task);
                        print('Extract urls: ref=' + task.url + ', urlsInPage = ' + str(len(url_tasks)))
                        for url_Task in url_tasks:
                            result = self.crawler_conf.engine.fetch(url_Task)
                            # save result
                            # TODO
                    depth = depth + 1
                
                
# test crawler
def crawl():
    conf = CrawlerConf()
    conf.max_depth = 1
    crawler = DefaultCrawler(conf)
    task_conf = TaskConf('www.baidu.com')
    task_conf.max_depth = 1
    url_task = UrlTask(task_conf)
    crawler.crawl(url_task)
    
if __name__ == '__main__':
    crawl()