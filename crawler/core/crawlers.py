from abc import ABCMeta
import re

from crawler.core.common import Crawler, TaskConf, CrawlMode, CrawlPolicy, \
    LoggerFactory
from crawler.core.http import DefaultHttpEngine, HtmlParser
from crawler.core.storage import CrawlerStorage
from crawler.core.utils import UniqIdGenerator


class DefaultCrawler(Crawler):
    '''
    Default crawler implementation class.
    References:
    1. http://en.wikipedia.org/wiki/List_of_HTTP_header_fields
    '''
    def __init__(self, crawler_conf):
        super(DefaultCrawler, self).__init__(crawler_conf)
        # set crawler name
        self._name = self._crawler_conf.crawler_name
        if not self._name:
            seed = self.__class__.__name__
            self._name  = 'crawler-' + str(UniqIdGenerator.next_id(seed))
        # set HTTP engine
        self._http_engine = self._crawler_conf.http_engine
        # set storage tool
        self.__storage = self._crawler_conf.storage
        # initialize crawler according to the mode
        if self._crawler_conf.mode == CrawlMode.SIMPLE:
            self._crawl_policy = SimpleCrawlPolicy(self)
        elif self._crawler_conf.mode == CrawlMode.STORAGE:
            # crawl and store page content
            if not self._http_engine:
                self._http_engine = DefaultHttpEngine()
            if not self.__storage:
                self.__storage = CrawlerStorage()
                self.__storage.initialize()
            # set internal fetcher
            self._crawl_policy = StorageCrawlPolicy(self)
            # internal storage fetcher implementation
        else:
            print('Undefined crawl mode: mode = ' + self._crawler_conf.mode)
    
    def get_name(self):
        return self._name
    
    def crawl(self, url_task):
        # crawl a url task built from the seed file
        task = url_task
        if task and task.url and self._crawl_policy.should_crawl(task.url):
            # invoke
            self._crawl_policy.fetch(task)
           
    def __str__(self):
        return 'Crawler[' + self._name + ']'
    

class AbstractCrawlPolicy(CrawlPolicy):
    '''
    Abstract crawl policy.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, crawler):
        super(AbstractCrawlPolicy, self).__init__(crawler)
        self._crawler_conf = self._crawler.get_crawler_conf()
        self._http_engine = self._crawler_conf.http_engine
        
    def __compute_max_depth(self, url_task):
        if not self._max_depth:
            if url_task.task_conf.max_depth:
                self._max_depth = url_task.task_conf.max_depth
            else:
                self._max_depth = self._crawler_conf.max_depth
        else:
            self._max_depth = self._crawler_conf.max_depth
    
    def fetch(self, url_task):
        task = url_task
        # fetch page
        self._http_engine.fetch(task)
        status_code = self._http_engine.get_status_code()
        # save result
        self.store(task)
        self.__compute_max_depth(task)
        if status_code and status_code == 200:
            if task.depth <= self._max_depth - 1:
                # extract and check urls
                urls = ResultParser.extract_urls(task.crawl_result)
                # normalize urls
                urls = ResultParser.normalize_urls(urls, task.url)
                # filter urls
                if not task.task_conf.cross_host_allowed:
                    urls = ResultParser.filter_urls(urls, task.task_conf.domain)
                waiting_crawled_urls = filter(self.should_crawl, urls)
                # build url tasks
                url_tasks = TaskFactory.build_url_tasks(task, waiting_crawled_urls);
                print('Extract urls: ref = ' + task.url + ', urls_in_page = ' + str(len(url_tasks)))
                for url_task in url_tasks:
                    self.fetch(url_task)
        elif status_code >= 300 and status_code < 400:
            # redirection
            location = self._http_engine.get_resp_header('Location')
            print('Redirection: localtion_url = ' + location)
            
    def store(self, url_task):
        status_code = self._http_engine.get_status_code()
        url_task.crawl_result.status_code = status_code
        if status_code and status_code == 200:
            url_task.crawl_result.binary_data = self._http_engine.get_data()
            #url_task.crawl_result.response_headers = None
            self._log_crawl(status_code, url_task.url)
        else:
            self._log_crawl(status_code, url_task.url)
        # collect crawled data
        # collect url data
        url_data = url_task.crawl_result.url_data
        url_data['url'] = url_task.url
        # collect page data
        page_data = url_task.crawl_result.page_data
        page_data['url'] = url_task.url
        page_data['status_code'] = status_code
        content_type = self._http_engine.get_resp_header('Content-Type')
        charset = self._extract_charset(content_type)
        if charset:
            page_data['charset'] = charset
            url_task.crawl_result.charset = charset
        etag = self._http_engine.get_resp_header('ETag')
        page_data['etag'] = etag
        last_modified = self._http_engine.get_resp_header('Last-Modified')
        page_data['last_modified'] = last_modified
        data = self._http_engine.get_data()
        if data:
            page_data['content'] = data
    
    def _extract_charset(self, content_type):
        encoding = 'utf-8'
        if content_type:
#             print('content_type = ' + content_type)
            charsets = re.findall(r'.*charset\s*=\s*[\'\"]*([^\'\"]+).*', content_type, re.I)
            if charsets:
                encoding = charsets[0].lower() 
        return encoding
    
    def _log_crawl(self, status_code, url):
        template = 'Crawled: status_code = {0}, url = {1}'
        print(template.format(status_code, url))      
    
        
class SimpleCrawlPolicy(AbstractCrawlPolicy):
    '''
    Simple crawl policy implementation.
    '''
    def __init__(self, crawler):
        super(SimpleCrawlPolicy, self).__init__(crawler)
        
    def should_crawl(self, url):
        return True
    
    def store(self, url_task):
        super().store(url_task)
        print('url_data = ' + str(url_task.crawl_result.url_data))
        print('page_data = ' + str(url_task.crawl_result.page_data))
    

class StorageCrawlPolicy(AbstractCrawlPolicy):
    '''
    Storage crawl policy implementation.
    '''
    def __init__(self, crawler):
        super(StorageCrawlPolicy, self).__init__(crawler)
        self._storage = crawler.get_crawler_conf().storage
        
    def should_crawl(self, url):
        if not self._storage.is_crawled(url):
            return True
        elif self._storage.should_crawl(url):
            return True
        else:
            return False
    
    def store(self, url_task):
        super().store(url_task)
        # store to database
        # store url data
        url_data = url_task.crawl_result.url_data
        self.__insert_url(**url_data)
        # store page data
        page_data = url_task.crawl_result.page_data
        self.__insert_page(**page_data)
        
    def __insert_page(self, **page_data):
        self._storage.save_page(**page_data)
    
    def __insert_url(self, **url_data):
        self._storage.save_url(**url_data)
    
        
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
    def build_url_tasks(cls, url_task, waiting_crawled_urls):
        url_tasks = []
        if not url_task and not url_task.crawl_result:
            return url_tasks
        if url_task.depth <= url_task.task_conf.max_depth:
            depth = url_task.depth + 1
            # build url tasks
            for url in waiting_crawled_urls:
                print('build url task: url = ' + url)
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
        self.response_headers = {}
        self.exceptions = []
        self.url_data = {}
        self.page_data = {}
        
    def __str__(self):
        return 'url = ' + self.url + ', charset=' + self.charset
    

class ResultParser:
    '''
    Parse result page content crawled by a crawler.
    '''
    BAD_CHARACTERS = ['\'', '\"', '>', '<', ' ']
    BAD_SUFFIX_NAMES = [
        '.zip', '.rar', '.iso', '.gz', '.tar', '.jar', 
        '.gzip', '.7z', '.cab', '.uue', '.bz2', '.z',
        '.rmvb', '.mkv', '.mp3', '.mp4', '.mov', '.flv',
        '.wmv', '.asf', '.csf', '.sts', '.swf', '.avi',
        '.ts', '.acm', '.adf', '.aiff', '.ani', '.dll', 
        '.so', '.emf', '.tiff', '.psd', '.pcx', '.wmf',
        '.png', '.gif', '.bmp', '.ico', '.jpg', '.jpeg',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt',
        '.ppt', '.pptx', '.mdf', '.exe', '.css', 
        '.java', '.cpp', '.py', '.rb', '.go', '.php',
        '.c', '.hpp', '.sh', '.pl', '.clj', '.h'
    ]
    
    @classmethod
    def extract_urls(cls, crawl_result):
        urls = []
        if crawl_result.status_code == 200:
            cls.__get_string_data(crawl_result)
            if len(crawl_result.string_data) > 0:
                urls = HtmlParser.extract_urls(crawl_result.string_data)
        return urls
    
    @classmethod
    def normalize_urls(cls, urls, base_url):
        return HtmlParser.normalize_urls(urls, base_url)
    
    @classmethod
    def filter_urls(cls, urls, domain):
        return filter(lambda url : url.find(domain) != -1, urls)
    
    @classmethod
    def extract_anchors(cls, crawl_result):
        anchors = []
        if crawl_result.starus_code == 200:
            cls.__get_string_data(crawl_result)
            if len(crawl_result.string_data) > 0:
                anchors = re.findall(r"<a.*?href=.*?<\/a>", crawl_result.string_data, re.I)
        return anchors
    
    @classmethod
    def __get_string_data(cls, crawl_result):
        string_data = ''
        data = crawl_result.binary_data
        if data:
            try:
                string_data = data.decode(crawl_result.charset)
            except UnicodeDecodeError as e:
                print(str(e))
        crawl_result.string_data = string_data



