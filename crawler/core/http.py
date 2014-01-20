import re
import urllib
from urllib.error import HTTPError
from urllib.parse import urljoin

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
    

class HtmlParser:
    '''
    HTML related parser tool.
    '''
    BAD_CHARACTERS = ['\'', '\"', '>', '<', ' ']
    BAD_SUFFIX_NAMES = [
        '.zip', '.rar', '.iso', '.gz', '.tar', '.jar', 
        '.gzip', '.7z', '.cab', '.uue', '.bz2', '.z',
        '.rmvb', '.mkv', '.mp3', '.mp4', '.mov', '.flv',
        '.wmv', '.asf', '.csf', '.sts', '.swf', '.avi',
        '.ts', '.acm', '.adf', '.aiff', '.ani', '.dll', 
        '.so', '.emf', '.tiff', '.psd', '.pcx', '.wmf',
        '.png', '.gif', '.bmp', '.ico', '.jpg', '.jpeg',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt',
        '.ppt', '.pptx', '.mdf', '.exe', '.css', 
        '.java', '.cpp', '.py', '.rb', '.go', '.php',
        '.c', '.cc', '.hpp', '.sh', '.pl', '.clj', '.h'
    ]
    
    @classmethod
    def extract_urls(cls, html):
        urls = []
        if html and len(html) > 0:
            all_urls = re.findall(r"<a.*?href=\s*[\"']*([^\"']+).*?<\/a>", html, re.I)
            for url in all_urls:
                if url and len(url.strip()) > 0:
                    urls.append(url)
        return urls
    
    @classmethod
    def normalize_urls(cls, urls, base_url=None):
        url_set = set()
        for url in urls:
            u = None
            # discard url with bad suffix name
            lowered_url = url.lower()
            for name in HtmlParser.BAD_SUFFIX_NAMES:
                if lowered_url.endswith(name):
                    continue
            # discard url containing bad characters
            bad_character_found = False
            for ch in HtmlParser.BAD_CHARACTERS:
                if url.find(ch) != -1:
                    bad_character_found = True
                    break
            if not bad_character_found:
                u = url
            # url starting with '#'
            if url.startswith('#'):
                continue
            if lowered_url.startswith('http://'):
                # url starting with 'http://'
                lowest_index = url.find('#')
                if lowest_index != -1:
                    u = url.split('#')[0]
            elif lowered_url.startswith('https://'):
                # url starting with 'https://'
                continue
            else:
                # join base url and a relative url
                if base_url:
                    u = urljoin(base_url, url)
            # collect normalized urls
            if u:
                url_set.add(u)
        return url_set
    
