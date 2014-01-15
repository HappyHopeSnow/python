import urllib
from urllib.error import HTTPError

from crawler.core.common import HttpEngine


class DefaultHttpEngine(HttpEngine):
    '''
    Default HTTP engine implementation.
    '''
    reqHeaders = {
        'Accept'             : 'text/plain',
        'Accept-Charset'     : 'utf-8',
        'Accept-Language'    : 'en-US;zh-CN',
        'Host'               : 'www.shiyanjun.cn',
        'Content-Length'     : '10240',
        'User-Agent'         : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
    }
    
    def __init__(self):
        super(DefaultHttpEngine, self).__init__()
        
    def fetch(self, url_task):
        url = url_task.url
        try:
            response = urllib.request.urlopen(url)
        except HTTPError as e:
            self._status_code = int(e.code)
            self._exceptions.append(e)
        except BaseException as e:
            self._exceptions.append(e)
        else:
            self._status_code = response.status
            for key in response.headers:
                self._resp_headers[key] = response.headers[key]
            data = response.read()
            if data:
                self._binary_data = data
    
    def reuse(self):
        if self._is_reuseable:
            # clear status
            self._initialize()
        else:
            raise BaseException('Can not be reused!')
    
