from crawler.core.storage import SQLite, CrawlerStorage


if __name__ == '__main__':
    SQLite.connect()
    SQLite.create_crawler_tables()
    
    # test insert a page
    def test_insert_page():
        store = CrawlerStorage()
        page = {
                'url' : 'http://baidu.com',
                'status_code' : 200,
                'charset' : 'utf-8',
                'etag' : 'FDSa12-kldjanJK8',
                'last_modified' : '2014-01-08 19:07:27'
            }
        store.save_page(**page)
    
    # test query a page
    def test_query_page():
        store = CrawlerStorage()
        url ='http://www.baidu.com'
        result = store.query_page(url)
        iterate(result)
    
    # test query all pages
    def test_query_all_pages():
        store = CrawlerStorage()
        result = store.query_all_pages()
        iterate(result)
            
    def test_query_all_urls():
        store = CrawlerStorage()
        result = store.query_all_urls()
        iterate(result)
            
    def iterate(result):
        for record in result:
            print(str(record))
            
    def test_is_crawled():
        store = CrawlerStorage()
        url ='http://www.baidu.com'
        is_crawled = store.is_crawled(url)
        print('is_crawled = ' + str(is_crawled) + ', url = ' + url)
    
    # stitch flag for test
    is_insert = False
    is_select = False
    is_crawled = False
    is_query_all_pages = False
    is_query_all_urls = True
        
    if is_insert:
        test_insert_page()
    if is_select:
        test_query_page()
    if is_query_all_pages:
        test_query_all_pages()
    if is_query_all_urls:
        test_query_all_urls()
    if is_crawled:
        test_is_crawled()