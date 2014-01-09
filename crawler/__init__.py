from crawler.common import CrawlerConf, TaskConf
from crawler.crawlers import DefaultCrawler, UrlTask
from crawler.manager import DefaultCrawlerManager


# test crawler
def crawl():
#     task_file = r'E:\git\python\crawler\data\seeds.conf'
#     manager = DefaultCrawlerManager(task_file)
    conf = CrawlerConf()
    conf.max_depth = 1
    crawler = DefaultCrawler(conf)
    task_conf = TaskConf('apache.org')
    task_conf.max_depth = 1
    url_task = UrlTask(task_conf)
    crawler.crawl(url_task)
    
if __name__ == '__main__':
    crawl()