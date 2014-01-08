from crawler.common import CrawlerManager, CrawlerConf
from crawler.crawlers import TaskFactory, DefaultCrawler
from crawler.http import DefaultHttpEngine
from crawler.storage import CrawlerStorage
from crawler.utils import UniqIdGenerator


class DefaultCrawlerManager(CrawlerManager):
    '''
    Default crawler manager implementation.
    '''
    
    def __init__(self, task_file='data/seeds.conf'):
        self.__storage = CrawlerStorage()
        self.__seed_tasks = TaskFactory.build_seeds(task_file)
        self.__create_engine() 
        self.__crawlers = {}
    
    def __create_engine(self):
        self.__http_engine = DefaultHttpEngine()
           
    def create_crawler(self):
        conf = CrawlerConf()
        conf.max_depth = 1
        seed = self.__class__.__name__
        name  = str(UniqIdGenerator.next_id(seed))
        crawler = DefaultCrawler(conf, name, self)
        self.__crawlers[name] = crawler
        return name
        
    def wait_for(self):
        for task in self.__seed_tasks:
            name = self.create_crawler()
            crawler = self.__crawlers.get(name)
            if crawler:
                crawler.crawl(task)
                self.notify_complete(name)
        
    def notify_complete(self, crawler_name):
        self.__crawlers.pop(crawler_name)
    
    def get_storage(self):
        return self.__http_engine
    
    def get_http_engine(self):
        return self.__storage
