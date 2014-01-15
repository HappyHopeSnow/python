from crawler.core.common import CrawlerConf, TaskConf
from crawler.core.crawlers import DefaultCrawler, UrlTask
from crawler.core.manager import DefaultCrawlerManager


# test crawler
def crawl():
#     task_file = r'E:\git\python\crawler\data\seeds.conf'
#     manager = DefaultCrawlerManager(task_file)
    conf = CrawlerConf()
    conf.max_depth = 1
    crawler = DefaultCrawler(conf)
    task_conf = TaskConf('www.163.com')
    task_conf.max_depth = 1
    url_task = UrlTask(task_conf)
    crawler.crawl(url_task)
    

def managed_crawl():
    task_file = r'E:\git\python\crawler\data\seeds.conf'
    manager = DefaultCrawlerManager(task_file)
    manager.wait_for()
    
if __name__ == '__main__':
#     crawl()
    managed_crawl()
