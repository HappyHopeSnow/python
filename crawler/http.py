import urllib
from urllib.error import HTTPError

from crawler.common import HttpEngine


class DefaultHttpEngine(HttpEngine):
    '''
    '''
    reqHeaders = {
        'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
    }
    
    def __init__(self):
        self.__initialize()
        
    def __initialize(self):
        self.__is_reuseable = True
        self.__status_code = None
        self.__resp_headers = {}
        self.__binary_data = None
        self.__exceptions = []
    
    def fetch(self, url_task):
        url = url_task.url
        try:
            response = urllib.request.urlopen(url)
        except HTTPError as e:
            self.__status_code = e.code
            self.__exceptions.append(e)
        except BaseException as e:
            self.__exceptions.append(e)
        else:
            self.__status_code = response.status
            for key in response.headers:
                self.__resp_headers[key] = response.headers[key]
            data = response.read()
            if data:
                self.__binary_data = data
    
    def get_status_code(self):
        return self.__status_code
    
    def get_resp_header(self, key):
        value = None
        if key:
            value = self.__resp_headers.get(key)
        return value
    
    def get_data(self):
        return self.__binary_data
    
    def is_reuseable(self):
        return self.__is_reuseable
        
    def reuse(self):
        if self.__is_reuseable:
            # clear status
            self.__initialize()
        else:
            raise BaseException('Can not be reused!')
    
