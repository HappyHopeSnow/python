from abc import ABCMeta, abstractmethod
import copy
from socket import socket


class TaskConf:
    '''
    A crawl task configuration object.
    '''
    def __init__(self, domain):
        self.domain = domain
        self.seed_task = None
        self.priority = 0
        self.max_depth = 0
        self.cross_host_allowed = False
        self.connect_timeout = 3000
        self.socket_timeout = 30000
    
    @classmethod
    def clone(self, task_conf):
        copier = None
        if task_conf:
            copier = copy.deepcopy(task_conf)
        return copier
        
    

class Task:
    '''
    A crawler task abstraction.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, task_conf):
        self.task_conf = task_conf
        self.domain = task_conf.domain
        self.url = None
        self.ip = None
    
    @abstractmethod
    def check(self):
        pass
    
    
class SeedTask(Task):
    '''
    A task encapsulates crawler related resources before starting
    to crawl pages of a domain.
    '''
    def __init__(self, task_conf):
        super(SeedTask, self).__init__(task_conf)
        # check invalidation of a domain
        domain = self.task_conf.domain
        if not domain:
            raise ValueError('Inputed domain is None!')
        if domain.startswith('https://'):
            raise ValueError('Unsupported HTTPS link!')
        # 
        if not domain.startswith('http://'):
            self.url = 'http://' + domain
            self.ip = socket.getaddrinfo(domain, 'http')[0][4][0]

        
class UrlTask(Task):
    '''
    A task encapsulates crawler related url resources before starting
    to crawl pages represented by a url.
    '''
    def __init__(self, task_conf):
        super(UrlTask, self).__init__(task_conf)
        self.seed_task = self.task_conf.seed_task
        

class TaskFactory:
    '''
    Build tasks from a given file.
    Here tasks has 2 types: SeedTask and UrlTask.
    '''
    @classmethod
    def build_seeds(cls, task_file):
        seed_tasks = []
        try:
            f = open(task_file, 'r')
        except:
            raise IOError('Error to open file: ' + task_file)
        for line in f:
            if line.strip().startswith('#'):
                continue
            a = line.strip().split('\s*,\s*')
            if len(a) == 5:
                domain = a[0].lower()
                # domain
                task_conf = TaskConf(domain)
                # priority
                task_conf.priority = int(a[1])
                # maxDepth
                task_conf.max_depth = int(a[2])
                # crossHostAllowed
                if a[3].lower() == 'true':
                    task_conf.cross_host_allowed = True
                elif a[3].lower() == 'false':
                    task_conf.cross_host_allowed = False
                # connectionTimeout
                task_conf.connect_timeout = int(a[4])
                # socketTimeout
                task_conf.socket_timeout = int(a[5])
                seed_task = SeedTask(task_conf)
                seed_tasks.append(seed_task)
        f.close()
        return seed_tasks
    
    @classmethod
    def build_url_tasks(cls, seed_task=None, crawl_result=None):
        url_tasks = []
        if not seed_task and not crawl_result:
            return url_tasks
        if seed_task:
            url_task = UrlTask(seed_task.task_conf)
            url_tasks.append(url_task)
        else:
            if crawl_result:
                parent = crawl_result.url_task
                if not parent:
                    parent = UrlTask()
                    parent.set_seed
                depth = parent.depth
            data = crawl_result.data
            # extract url from the source code of a page
            
        return url_tasks
        
        
    