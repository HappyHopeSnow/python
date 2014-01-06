from abc import ABCMeta, abstractmethod

from crawler.common.task import TaskFactory
from crawler.http.client import DefaultHttpEngine
from crawler.utils.sequences import UniqIdGenerator


class CrawlerConf:
    '''
    Configure a crawler's behaviors.
    '''
    def __init__(self):
        self.engine = DefaultHttpEngine()
        self.max_depth = 1
        

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
    def __init__(self, url_task):
        self.url_task = url_task
        self.data = None
        self.status_code = None
        self.charset = 'UTF-8'
        self.urls = []
        

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
            
    def crawl(self, seed_task):
        # build urlTask from a seedTask
        tasks = TaskFactory.build_url_tasks(seed_task)
        if tasks and len(tasks) == 1:
            task = tasks[0]
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
                    url_tasks = TaskFactory.build_url_tasks(seed_task, result);
                    for url_Task in url_tasks:
                        result = self.crawler_conf.engine().fetch(url_Task)
                        # save result
                        # TODO
                depth = depth + 1
                
        

