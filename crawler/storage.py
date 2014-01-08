from datetime import datetime, date, time
import hashlib
import sqlite3

from crawler.common import Storage


class CrawlerStorage(Storage):
    
    def initialize(self):
        SQLite.connect()
        SQLite.create_crawler_tables()
        
    def save_page(self, **page_data):
        url = page_data.get('url', None)
        if url:
            pk = self.__md5(url)
            content = page_data.get('content', '')
            status_code = page_data.get('status_code', 0)
            charset = page_data.get('charset', '')
            etag = page_data.get('etag', '')
            last_modified = page_data.get('last_modified', '')
            create_time = self.__now_datetime()
            update_time = create_time
            sql = 'INSERT INTO page('
            sql += 'id, url, content, status_code, charset, etag, last_modified, create_time, update_time'
            sql += ') VALUES ('
            sql += '\'' + pk + '\','
            sql += '\'' + url + '\','
            sql += '\'' + content + '\','
            sql += status_code
            sql += '\'' + charset + '\','
            sql += '\'' + etag + '\','
            sql += '\'' + last_modified + '\','
            sql += '\'' + create_time + '\','
            sql += '\'' + update_time + '\''
            sql += ')'
            SQLite.execute_sql(sql)
    
    def save_url(self, **url_data):
        url = url_data.get('url', None)
        if url:
            md5 = self.__md5(url)
            create_time = self.__now_datetime()
            update_time = create_time
            sql = 'INSERT INTO url('
            sql += 'md5, url, create_time, update_time'
            sql += ') VALUES ('
            sql += '\'' + md5 + '\','
            sql += '\'' + url + '\','
            sql += '\'' + create_time + '\','
            sql += '\'' + update_time + '\''
            sql += ')'
            SQLite.execute_sql(sql)
        
    def __now_datetime(self):
        #http://docs.python.org/3/library/datetime.html
        now = datetime.now()
        str_date = now.strftime("%y-%m-%d %H:%M:%S")
        return str_date
        
        
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