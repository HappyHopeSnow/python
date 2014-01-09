from datetime import datetime
import hashlib
import sqlite3

from crawler.common import Storage


class CrawlerStorage(Storage):
    
    __charset = 'UTF-8'
    __insert_page_sql = '''
        INSERT INTO page(
        id, url, content, status_code, charset, etag, last_modified, create_time, update_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    __update_page_sql = '''
        UPDATE page SET
        content = ?, status_code = ?, charset = ?, etag = ?, 
        last_modified = ?, update_time = ? 
        WHERE id = ?
    '''
    __insert_url_sql = '''
        INSERT INTO url(md5, url, create_time, update_time) VALUES (?, ?, ?, ?)
    '''
    __select_page_sql = '''
        SELECT * FROM page WHERE id = ?
    '''
    __select_all_page_sql = '''
        SELECT * FROM page
    '''
    __select_url_sql = '''
        SELECT * FROM url WHERE md5 = ?
    '''
    __select_all_url_sql = '''
        SELECT * FROM url
    '''
    
    def initialize(self):
        SQLite.connect()
        SQLite.create_crawler_tables()
    
    def query_page(self, url):
        md5 = self.__md5(url)
        value = (md5, )
        result = SQLite.execute_query_sql(CrawlerStorage.__select_page_sql, value)
        return result
    
    def query_all_pages(self):
        return SQLite.execute_query_sql(CrawlerStorage.__select_all_page_sql)
    
    def query_all_urls(self):
        return SQLite.execute_query_sql(CrawlerStorage.__select_all_url_sql)
    
    def save_page(self, **page_data):
        url = page_data.get('url', None)
        if url:
            pk = self.__md5(url)
            # binary data
            content = page_data.get('content', '')
            status_code = page_data.get('status_code', 0)
            charset = page_data.get('charset', '')
            etag = page_data.get('etag', '')
            last_modified = page_data.get('last_modified', '')
            create_time = self.__now_datetime()
            update_time = create_time
            if not self.__is_need_update(url):
                sql = CrawlerStorage.__insert_page_sql
                value = (pk, url, content, status_code, charset, etag, last_modified, create_time, update_time)
                print('INSERT page values: ' + str(value))
            else:
                sql = CrawlerStorage.__update_page_sql
                value = (content, status_code, charset, etag, last_modified, update_time, pk)
                print('UPDATE page values: url= ' + url + ', ' + str(value))
            SQLite.execute_dml_sql(sql, value)
    
    def __is_need_update(self, url):
        is_needed = False
        result = self.query_page(url)
        status_code = 0
        if len(result) == 0:
            is_needed = False
        elif len(result) > 0:
            status_code = result[0][3]
        if status_code != 200:
            is_needed = True
        return is_needed
        
    def save_url(self, **url_data):
        url = url_data.get('url')
        if url and not self.is_crawled(url):
            md5 = self.__md5(url)
            create_time = self.__now_datetime()
            update_time = create_time
            sql = CrawlerStorage.__insert_url_sql
            value = (md5, url, create_time, update_time)
            print('INSERT url values: ' + str(value))
            SQLite.execute_dml_sql(sql, value)
        
    def __now_datetime(self):
        #http://docs.python.org/3/library/datetime.html
        now = datetime.now()
        str_date = now.strftime("%y-%m-%d %H:%M:%S")
        return str_date
        
        
    def __md5(self, url):
        md5 = None
        if url:
            md5 = hashlib.md5(url.encode(CrawlerStorage.__charset)).hexdigest()
        return md5
    
    def should_crawl(self, url):
        should = False
        md5 = self.__md5(url)
        value = (md5, )
        result = SQLite.execute_query_sql(CrawlerStorage.__select_page_sql, value)
        status_code = 0
        if len(result) != 0:
            status_code = result[0][3]
        if status_code != 200:
            should = True
        return should
    
    def is_crawled(self, url):
        md5 = self.__md5(url)
        value = (md5, )
        result = SQLite.execute_query_sql(CrawlerStorage.__select_url_sql, value)
        return len(result) != 0
    
    def close(self):
        SQLite.close()
        

class SQLite:
    __db = 'crawler.db'
    __page_sql = '''
        create table if not exists page (
            id text primary key, 
            url text unique, 
            content blob, 
            status_code integer, 
            charset text,
            etag text, 
            last_modified text, 
            create_time text,
            update_time text)
    '''
    __url_sql = '''
        create table if not exists url (
            md5 text primary key, 
            url text unique,
            create_time text,
            update_time text)
    '''
    __tables = {
              'page' : __page_sql, 
              'url' : __url_sql
              }
    connection = None
    
    @classmethod
    def connect(cls, db='crawler.db'):
        if db:
            cls.__db = db
        if not cls.connection:
            try:
                cls.connection = sqlite3.connect(cls.__db)
            except sqlite3.Error as e:
                print('Fail to connect db ' + cls.db + ': ', e.args[0])
        return cls.connection
    
    @classmethod
    def create_crawler_tables(cls):
        for table in cls.__tables:
            cls.__create_table(table)
       
    @classmethod         
    def __create_table(cls, table):
        cls.connect(cls.__db)
        cursor = cls.connection.cursor()
        if cls.__tables.get(table):
            try:
                cursor.execute(cls.__tables[table])
            except sqlite3.Error as e:
                print('Fail to create table ' + table, e.args[0]) 
    
    @classmethod
    def execute_dml_sql(cls, sql, value):
        cls.connect(cls.__db)
        cursor = cls.connection.cursor()
        try:
            cursor.execute(sql, value)
        except sqlite3.Error as e:
            print('Fail to execute sql: ' + sql, e.args[0]) 
        else:
            cursor.close()
    
    @classmethod
    def execute_query_sql(cls, sql, value=None):
        cls.connect(cls.__db)
        cursor = cls.connection.cursor()
        try:
            if value:
                cursor.execute(sql, value)
            else:
                cursor.execute(sql)
        except sqlite3.Error as e:
            print('Fail to execute sql: ' + sql, e.args[0]) 
        else:
            result = list(cursor)
            cursor.close()
            return result
    
    @classmethod
    def close(cls):
        if cls.connection:
            cls.connection.close()



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
        url ='http://apache.org'
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
        url ='http://apache.org'
        is_crawled = store.is_crawled(url)
        print('is_crawled = ' + str(is_crawled) + ', url = ' + url)
    
    # stitch flag for test
    is_insert = False
    is_select = False
    is_crawled = False
    is_query_all_pages = True
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