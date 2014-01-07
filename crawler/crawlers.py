import re

from crawler.common import Crawler, TaskConf
from crawler.http import DefaultHttpEngine
from crawler.utils import UniqIdGenerator


class DefaultCrawler(Crawler):
    '''
    Default crawler implementation class.
    References:
    1. http://en.wikipedia.org/wiki/List_of_HTTP_header_fields
    '''
    def __init__(self, conf, name=None):
        super(DefaultCrawler, self).__init__(conf)
        # initialize HTTP engine
        self.__http_engine = self.__create_engine()
        self.name = name
        if not name:
            seed = self.__class__.__name__
            name  = str(UniqIdGenerator.next_id(seed))
        print('Create crawler: id = ' + name)
        self.__max_depth = self.crawler_conf.max_depth
        
    def __create_engine(self):
        self.__http_engine = DefaultHttpEngine()
            
    def crawl(self, url_task):
        # crawl a url task built from the seed file
        task = url_task
        if task:
            # compute max depth of crawling pages
            if task.task_conf.max_depth:
                # override default max depth configuration
                self.__max_depth = task.task_conf.max_depth
            # invoke
            self.__fetch_all(task)
            
    def __fetch_all(self, task):
        self.__fetch(task)
        status_code = self.__http_engine.get_status_code()
        # save result
        self.__store(task)
        if status_code and status_code == 200:
            if task.depth <= self.__max_depth - 1:
                url_tasks = TaskFactory.build_url_tasks(task);
                print('Extract urls: ref=' + task.url + ', urlsInPage = ' + str(len(url_tasks)))
                for url_task in url_tasks:
                    self.__fetch_all(url_task)
    
    def __fetch(self, url_task):
        if not self.__http_engine:
            self.__create_engine()
        else:
            if self.__http_engine.is_reuseable():
                self.__http_engine.reuse()
            else :
                self.__create_engine()
        # fetch page
        self.__http_engine.fetch(url_task)
        
    def __store(self, url_task):
        status_code = self.__http_engine.get_status_code()
        url_task.crawl_result.status_code = status_code
        if status_code and status_code == 200:
            url_task.crawl_result.binary_data = self.__http_engine.get_data()
            #url_task.crawl_result.response_headers = None
            print('Crawl page: status = SUCCESS, url = ' + url_task.url)
        else:
            print('Crawl page: status = FAILURE, url = ' + url_task.url)
        # TODO
        # store to DB
                    
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
            resultParser = ResultParser()
            urls = resultParser.extract_urls(url_task.crawl_result)
            for url in urls:
                print('Crawl page: url = ' + url)
                conf = TaskConf.clone(url, url_task.task_conf)
                task = UrlTask(conf)
                task.depth = depth
                url_tasks.append(task)
        return url_tasks
    
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
    

class ResultParser:
    
    def extract_urls(self, crawl_result):
        urls = []
        if crawl_result.status_code == 200:
            self.__get_string_data(crawl_result)
            if len(crawl_result.string_data) > 0:
                all_urls = re.findall(r"<a.*?href=\s*[\"']*([^\"']+).*?<\/a>", crawl_result.string_data, re.I)
                for url in all_urls:
                    if url and self.__is_valid_url(url.strip()):
                        urls.append(url)
        return urls
    
    def __is_valid_url(self, url): 
        is_valid = False
        if url:
            is_valid = url.startswith('http://') 
        return is_valid
        #and url.startswith('#') and url.startswith('/')
    
    def extract_anchors(self, crawl_result):
        anchors = []
        if crawl_result.starus_code == 200:
            self.__get_string_data(crawl_result)
            if len(crawl_result.string_data) > 0:
                anchors = re.findall(r"<a.*?href=.*?<\/a>", crawl_result.string_data, re.I)
        return anchors
    
    def __get_string_data(self, crawl_result):
        string_data = ''
        data = crawl_result.binary_data
        if data:
            string_data = data.decode(crawl_result.charset)
        crawl_result.string_data = string_data



