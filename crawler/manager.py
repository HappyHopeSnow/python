import logging

from crawler.common import CrawlerManager, CrawlerConf
from crawler.crawlers import TaskFactory, DefaultCrawler
from crawler.http import DefaultHttpEngine
from crawler.storage import CrawlerStorage
from crawler.utils import UniqIdGenerator


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
    
    def __create_engine(self):
        self._http_engine = DefaultHttpEngine()
           
    def create_crawler(self, task):
        conf = CrawlerConf()
        conf.max_depth = task.task_conf.max_depth
        seed = self.__class__.__name__
        name  = 'crawler-' + str(UniqIdGenerator.next_id(seed))
        DefaultCrawlerManager.__LOG.info('Manager create crawler: #' + name)
        crawler = DefaultCrawler(conf, name, self)
        self._crawlers[name] = crawler
        return name
        
    def wait_for(self):
        for task in self._seed_tasks:
            name = self.create_crawler(task)
            crawler = self._crawlers.get(name)
            if crawler:
                crawler.crawl(task)
                self.notify_complete(name)
        # close database
        self._storage.close()
        
    def notify_complete(self, crawler_name):
        self._crawlers.pop(crawler_name)
    
