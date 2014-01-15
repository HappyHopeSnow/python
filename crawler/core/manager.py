import logging

from crawler.core.common import CrawlerManager, CrawlerConf
from crawler.core.crawlers import TaskFactory, DefaultCrawler
from crawler.core.http import DefaultHttpEngine
from crawler.core.storage import CrawlerStorage
from crawler.core.utils import UniqIdGenerator


class DefaultCrawlerManager(CrawlerManager):
    '''
    Default crawler manager implementation.
    '''
    __FORMAT = ''
    __LOG = logging.getLogger(__name__)
    
    def __init__(self, task_file='data/seeds.conf'):
        super(DefaultCrawlerManager, self).__init__(task_file)
        self._storage = CrawlerStorage()
        self._storage.initialize()
        self._seed_tasks = TaskFactory.build_seeds(task_file)
        self.__create_engine()
        # initialize default crawler conf
        self.__crawler_conf = CrawlerConf()
        self.__crawler_conf.http_engine = self._http_engine
        self.__crawler_conf.storage = self._storage
        seed = self.__class__.__name__
        self.__crawler_conf.crawler_name =  'crawler-' + str(UniqIdGenerator.next_id(seed))
    
    def __create_engine(self):
        self._http_engine = DefaultHttpEngine()
           
    def create_crawler(self, task):
        conf = CrawlerConf.clone(self.__crawler_conf)
        crawler = DefaultCrawler(conf)
        return crawler
        
    def wait_for(self):
        for task in self._seed_tasks:
            crawler = self.create_crawler(task)
            self._crawlers[crawler.get_name()] = crawler
            if crawler:
                crawler.crawl(task)
                self.notify_complete(crawler.get_name())
        # close database
        self._storage.close()
        
    def notify_complete(self, crawler_name):
        self._crawlers.pop(crawler_name)
    
