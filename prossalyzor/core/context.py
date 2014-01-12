from abc import ABCMeta
import copy

from prossalyzor.core.common import Context


class AbstractContext(Context):
    '''
    Abstract context object implementation. It implements some
    basic methods which a context object behaves.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self):
        super(AbstractContext, self).__init__()
        
    def get(self, key, value=None):
        return self._settings.get(key, value)
    
    def set(self, key, value, override=True):
        if override:
            self._settings[key] = value
        else:
            v = self._settings.get(key)
            if v is not None:
                raise ValueError('Setting existed: key = ' + key + ', value = ' + str(v))
            else:
                self._settings[key] = value
    
    def clone(self):
        copier = copy.deepcopy(self)
        return copier
            
                
class TaskContext(AbstractContext):
    '''
    Configuration object held by a task.
    '''
    def __init__(self, job_context):
        super(TaskContext, self).__init__()
        self.__job_context = job_context
        
    def get_job_context(self):
        return self.__job_context
    
                

class JobContext(AbstractContext):
    '''
    Configuration object held by a task.
    '''
    def __init__(self):
        super(JobContext, self).__init__()


    