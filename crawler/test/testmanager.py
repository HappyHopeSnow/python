from crawler.core.manager import DefaultCrawlerManager


def managed_crawl():
    task_file = r'E:\git\python\crawler\data\seeds.conf'
    manager = DefaultCrawlerManager(task_file)
    manager.wait_for()
    
if __name__ == '__main__':
    managed_crawl()