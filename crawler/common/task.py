from abc import ABCMeta, abstractmethod
from socket import socket


class TaskConf:
    '''
    A crawl task configuration object.
    '''
    def __init__(self, domain):
        self.domain = domain
        self.priority = 0
        self.maxDepth = 0
        self.crossHostAllowed = False
        self.connectTimeout = 3000
        self.socketTimeout = 30000

class Task:
    '''
    A crawler task abstraction.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.depth = 0
        self.url = None
    
    @abstractmethod
    def check(self):
        pass
    
    def getUrl(self):
        return self.url
    
    
class SeedTask(Task):
    '''
    A task encapsulates crawler related resources before starting
    to crawl pages of a domain.
    '''
    def __init__(self, taskConf):
        super(SeedTask, self).__init__()
        self.taskConf = taskConf
        # check invalidation of a domain
        domain = taskConf.domain
        if domain is None:
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
    def __init__(self, seedTask):
        super(UrlTask, self).__init__()
        self.seedTask = seedTask
        

class TaskFactory:
    '''
    Build tasks from a given file.
    Here tasks has 2 types: SeedTask and UrlTask.
    '''
    
    @classmethod
    def buildSeeds(cls, taskFile):
        seedTasks = []
        try:
            f = open(taskFile, 'r')
        except:
            raise IOError('Error to open file: ' + taskFile)
        for line in f:
            if line.strip().startswith('#'):
                continue
            a = line.strip().split('\s*,\s*')
            if len(a) == 5:
                domain = a[0].lower()
                # domain
                taskConf = TaskConf(domain)
                # priority
                taskConf.priority = int(a[1])
                # maxDepth
                taskConf.maxDepth = int(a[2])
                # crossHostAllowed
                if a[3].lower() == 'true':
                    taskConf.crossHostAllowed = True
                elif a[4].lower() == 'false':
                    taskConf.crossHostAllowed = False
                # connectionTimeout
                taskConf.connectTimeout = int(a[5])
                # socketTimeout
                taskConf.socketTimeout = int(a[6])
                seedTask = SeedTask(taskConf)
                seedTasks.append(seedTask)
        f.close()
        return seedTasks
    
    @classmethod
    def buildUrlTasks(cls, crawlResult):
        urlTasks = []
        depth = crawlResult.urlTask.depth
        data = crawlResult.data
        responseHeaders = crawlResult.responseHeaders
        # extract url from the source code of a page
        
        return urlTasks
        
        
    