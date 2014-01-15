import re

from crawler.common import Crawler, TaskConf
from crawler.http import DefaultHttpEngine
from crawler.storage import CrawlerStorage
from crawler.utils import UniqIdGenerator


class DefaultCrawler(Crawler):
    '''
    Default crawler implementation class.
    References:
    1. http://en.wikipedia.org/wiki/List_of_HTTP_header_fields
    '''
    def __init__(self, crawler_conf, name=None, manager=None):
        super(DefaultCrawler, self).__init__(crawler_conf, name, manager)
        if manager:
            self._manager = manager
            self._storage = self._manager.get_storage()
            # initialize HTTP engine
            self.__http_engine = self._manager.get_http_engine()
        else:
            self.__http_engine = DefaultHttpEngine()
            self._storage = CrawlerStorage()
            self._storage.initialize()
        self.name = name
        if not name:
            seed = self.__class__.__name__
            name  = 'crawler-' + str(UniqIdGenerator.next_id(seed))
        print('Create crawler: #' + name)
        self.__max_depth = self._crawler_conf.max_depth
    
    def __should_try_to_crawl(self, url):
        if not self._storage.is_crawled(url):
            return True
        elif self._storage.should_crawl(url):
            return True
        else:
            return False
           
    def crawl(self, url_task):
        # crawl a url task built from the seed file
        task = url_task
        if task and task.url and self.__should_try_to_crawl(url_task.url):
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
                url_tasks = TaskFactory.build_url_tasks(task, self);
                print('Extract urls: ref=' + task.url + ', urlsInPage = ' + str(len(url_tasks)))
                for url_task in url_tasks:
                    self.__fetch_all(url_task)
        elif status_code >= 300 and status_code < 400:
            # redirection
            location = self.__http_engine.get_resp_header('Location')
            print('Redirection: localtion_url = ' + location)
    
    def __fetch(self, url_task):
        if self.__http_engine.is_reuseable():
            self.__http_engine.reuse()
        else:
            self.__create_engine()
        # fetch page
        self.__http_engine.fetch(url_task)
    
    def __log_crawl(self, status_code, url):
        template = 'Crawled: status_code = {0}, url = {1}'
        print(template.format(status_code, url))
         
    def __store(self, url_task):
        status_code = self.__http_engine.get_status_code()
        url_task.crawl_result.status_code = status_code
        if status_code and status_code == 200:
            url_task.crawl_result.binary_data = self.__http_engine.get_data()
            #url_task.crawl_result.response_headers = None
            self.__log_crawl(status_code, url_task.url)
        else:
            self.__log_crawl(status_code, url_task.url)
        # store to database
        # store url data
        url_data = {}
        url_data['url'] = url_task.url
        self.__insert_url(**url_data)
        # store page data
        page_data = {}
        page_data['url'] = url_task.url
        page_data['status_code'] = status_code
        content_type = self.__http_engine.get_resp_header('Content-Type')
        charset = self.__extract_charset(content_type)
        if charset:
            page_data['charset'] = charset
            url_task.crawl_result.charset = charset
        etag = self.__http_engine.get_resp_header('ETag')
        page_data['etag'] = etag
        last_modified = self.__http_engine.get_resp_header('Last-Modified')
        page_data['last_modified'] = last_modified
        data = self.__http_engine.get_data()
        if data:
            page_data['content'] = data
        self.__insert_page(**page_data)
        
    def __insert_page(self, **page_data):
        self._storage.save_page(**page_data)
    
    def __insert_url(self, **url_data):
        self._storage.save_url(**url_data)
    
    def __extract_charset(self, content_type):
        encoding = 'utf-8'
        if content_type:
#             print('content_type = ' + content_type)
            charsets = re.findall(r'.*charset\s*=\s*[\'\"]*([^\'\"]+).*', content_type, re.I)
            if charsets:
                encoding = charsets[0].lower() 
        return encoding
           
    def __str__(self):
        return 'Crawler[' + self.name + ']'
    
                    
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
    def build_url_tasks(cls, url_task, crawler):
        url_tasks = []
        if not url_task and not url_task.crawl_result:
            return url_tasks
        if url_task.depth <= url_task.task_conf.max_depth:
            depth = url_task.depth + 1
            # extract url from the page source data
            resultParser = ResultParser()
            urls = resultParser.extract_urls(url_task.crawl_result)
            for url in urls:
                is_url_crawled = cls.__is_url_crawled(url, crawler)
                if not is_url_crawled:
                    print('Crawl page: url = ' + url)
                    conf = TaskConf.clone(url, url_task.task_conf)
                    task = UrlTask(conf)
                    task.depth = depth
                    url_tasks.append(task)
        return url_tasks
    
    
    @classmethod
    def __is_url_crawled(cls, url, crawler):
        try:
            storage = cls.__get_storage(crawler)
        except BaseException as e:
            print(str(e))
        if storage.is_crawled(url):
            return True
        else:
            return False
        
    @classmethod
    def __get_storage(cls, crawler):
        manager = crawler.get_manager()
        if not manager:
            storage = CrawlerStorage()
        else:
            storage = manager.get_storage()
        return storage
    
    
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



