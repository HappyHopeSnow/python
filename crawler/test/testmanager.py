
from crawler.core.common import CrawlMode
from crawler.core.http import DefaultHttpEngine
from crawler.core.manager import DefaultCrawlerManager, Key
from crawler.core.storage import CrawlerStorage


def managed_crawl():
    task_file = r'E:\git\python\crawler\data\seeds.conf'
    settings = {
        Key.CRAWLER_CRAWL_MODE          :   CrawlMode.STORAGE,
        Key.CRAWLER_TASK_FILE           :   task_file,
        Key.CRAWLER_HTTP_ENGINE_CLASS   :   DefaultHttpEngine,
        Key.CRAWLER_STORAGE_CLASS       :   CrawlerStorage
    }
    manager = DefaultCrawlerManager(settings)
    manager.wait_for()
    
if __name__ == '__main__':
    managed_crawl()