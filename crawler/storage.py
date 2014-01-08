import hashlib
import sqlite3

from crawler.common import Storage


class CrawlerStorage(Storage):
    
    def initialize(self):
        SQLite.connect()
        SQLite.create_crawler_tables()
        
    def save_page(self, **page_data):
        url = page_data['url']
        if url:
            pk = self.__md5(url)
            content = page_data['content']
            status_code = page_data['status_code']
            charset = page_data['charset']
            etag = page_data['etag']
            last_modified = page_data['last_modified']
            sql = 'INSERT INTO page VALUES ('
            SQLite.execute_sql(sql)
    
    def save_url(self, **url_data):
        url = url_data['url']
        if url:
            md5 = self.__md5(url)
        sql = 'INSERT INTO url VALUES ('
        SQLite.execute_sql(sql)
        
    def __md5(self, url):
        md5 = None
        if url:
            md5 = hashlib.md5(url).hexdigest()
        return md5
    
    def is_crawled(self, url):
        pass
    

class SQLite:
    __db = 'crawler.db'
    __page_sql = '''
        create table if not exists page (
            id text, 
            url text, 
            content text, 
            status_code integer, 
            charset text,
            etag text, 
            last_modified text, 
            create_time text,
            update_time text)
    '''
    __url_sql = '''
        create table if not exists url (
            md5 text, 
            url text, 
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
    def execute_sql(cls, sql):
        cls.connect(cls.__db)
        cursor = cls.connection.cursor()
        try:
            cursor.execute(sql)
        except sqlite3.Error as e:
            print('Fail to execute sql: ' + sql, e.args[0]) 
            
    

if __name__ == '__main__':
    SQLite.connect()
    SQLite.create_crawler_tables()