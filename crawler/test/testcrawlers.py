from crawler.core.common import CrawlerConf, TaskConf, CrawlMode
from crawler.core.crawlers import DefaultCrawler, UrlTask
from crawler.core.http import DefaultHttpEngine


# test crawler
def crawl():
    crawler_conf = CrawlerConf()
    crawler_conf.mode = CrawlMode.SIMPLE
    crawler_conf.max_depth = 1
    crawler_conf.http_engine = DefaultHttpEngine()
    crawler_conf.storage = None
    crawler = DefaultCrawler(crawler_conf)
    task_conf = TaskConf('www.163.com')
    task_conf.max_depth = 1
    url_task = UrlTask(task_conf)
    crawler.crawl(url_task)

if __name__ == '__main__':
    crawl()