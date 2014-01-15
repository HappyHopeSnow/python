import logging

from crawler.core.common import CrawlerManager, CrawlerConf, Key
from crawler.core.crawlers import TaskFactory, DefaultCrawler
from crawler.core.utils import UniqIdGenerator


class DefaultCrawlerManager(CrawlerManager):
    '''
    Default crawler manager implementation.
    '''
    __FORMAT = ''
    __LOG = logging.getLogger(__name__)
    
    def __init__(self, settings):
        super(DefaultCrawlerManager, self).__init__(settings)
        task_file = settings[Key.CRAWLER_TASK_FILE]
        self._seed_tasks = TaskFactory.build_seeds(task_file)
        self._storage = settings[Key.CRAWLER_STORAGE_CLASS]()
        self._storage.initialize()
        self._http_engine = settings[Key.CRAWLER_HTTP_ENGINE_CLASS]()
        # initialize default crawler conf
        self.__crawler_conf = CrawlerConf()
        self.__crawler_conf.mode = settings[Key.CRAWLER_CRAWL_MODE]
        self.__crawler_conf.http_engine = self._http_engine
        self.__crawler_conf.storage = self._storage
        seed = self.__class__.__name__
        self.__crawler_conf.crawler_name =  'crawler-' + str(UniqIdGenerator.next_id(seed))
    
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
    
