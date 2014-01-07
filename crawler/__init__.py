from crawler.common import CrawlerConf, TaskConf
from crawler.crawlers import DefaultCrawler, UrlTask


# test crawler
def crawl():
    conf = CrawlerConf()
    conf.max_depth = 1
    crawler = DefaultCrawler(conf)
    task_conf = TaskConf('www.baidu.com')
    task_conf.max_depth = 1
    url_task = UrlTask(task_conf)
    crawler.crawl(url_task)
    
if __name__ == '__main__':
    crawl()