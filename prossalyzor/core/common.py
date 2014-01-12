from abc import ABCMeta, abstractmethod
from threading import Lock


class Configurable:
    '''
    For a object which implements this interface, it supports
    to be configured.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, context):
        self._context = context
        
    def get_context(self):
        return self._context
    

class Status:
    UNKNOWN = 0
    SUCCESS = 1
    FAILURE = 2
    

class Counter:
    TOTAL = 0
    SUCCESS = 1
    FAILURE = 2
    
    
class Stat:
    '''
    Process processing statistics information.
    '''
    def __init__(self):
        self.__lock = Lock()
        self._total_count = 0
        self._success_count = 0
        self._failure_count = 0
        
    def inc(self, result):
        self.add(result, 1)
            
    def add(self, counter, value): 
        with self.__lock:
            if counter == Counter.SUCCESS:
                self._success_count += value
            elif counter == Counter.FAILURE:
                self._failure_count += value
            else :
                raise ValueError('Unsupported counter: counter = ' + counter)
            self._total_count += value   
            
    def get_count(self, counter):
        count = 0
        if counter == Counter.SUCCESS:
            count = self._success_count
        elif counter == Counter.FAILURE:
            count = self._failure_count
        elif counter == Counter.TOTAL:
            count = self._total_count
        else:
            raise ValueError('Undefined counter: counter = ' + counter)
        return count
    
       
class Result:
    '''
    Processor execution result.
    '''
    def __init__(self):
        self.status = Status.UNKNOWN
        self.stat = Stat()
        
    
class Processor(Configurable):
    '''
    A processor abstraction. Any processor can process
    any domain related things, such as events, communications,
    data analysis, etc
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, context):
        super(Processor, self).__init__(context)
        self._result = Result()
        
    @abstractmethod
    def process(self):
        pass
        
    def get_result(self):
        return self._result
    
        
class Job(Processor):
    '''
    Job object abstraction. Usually a Job instance can hold
    a Task instance list, including a ordered Task linked list,
    or a randomly organized Task collection.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, context):
        super(Task, self).__init__(context)
        
        
class Scheduler(Configurable): 
    '''
    Job scheduler.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, context):
        super(Scheduler, self).__init__(context) 
    
    @abstractmethod
    def schedule(self):
        pass
    

class Task(Processor):
    '''
    Task object abstraction. In general, a Task object is a minimum 
    unit of runtime processing, and it can be organized, such as chained
    style, randomly grouped style, and held by a Job instance.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, context):
        super(Task, self).__init__(context)
        

class Context:
    '''
    Configuration object protocol. a Context object
    held by a job, or a task.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self._settings = {}
    
    @abstractmethod
    def get(self, key, value=None):
        pass
    
    @abstractmethod
    def set(self, key, value):
        pass
    
    @abstractmethod
    def clone(self):
        pass
        
    
class Executor(Configurable):
    '''
    Executor abstraction. A Executor can execute a Job object, a
    Task object, which separates the responsibilities between Processor
    and Executor. A Job and A Task are both Processor objects. 
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, context):
        super(Executor, self).__init__(context)
    
    @abstractmethod
    def execute(self, processor, callback):
        '''
            Execute a submitted processor object.
        '''
        pass


class PoolExecutor(Executor):
    '''
    Executor pool abstraction, which manages multiple Executors and
    reuse the Executor instances.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, context):
        super(PoolExecutor, self).__init__(context)
        
    @abstractmethod
    def shutdown(self):
        pass
    
    
class Input(Configurable):
    '''
    Input specification protocol. About the customized input
    specification, its object should get settings from a configured
    Context object. 
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, context):
        super(Input, self).__init__(context)
    
    @abstractmethod
    def input(self):
        pass
    

class Output(Configurable):
    '''
    Output specification protocol. About the customized output
    specification, its object should get settings from a configured
    Context object. 
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, context):
        super(Output, self).__init__(context)
        
    def output(self):
        pass  

