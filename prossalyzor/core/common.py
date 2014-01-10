from abc import ABCMeta, abstractmethod


class Executor:
    '''
    Executor abstraction.
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def execute(self, task, callback):
        '''
            Execute a submitted task object.
        '''
        pass


class ExecutorPool(Executor):
    '''
    Executor pool abstraction.
    '''
    __metaclass__ = ABCMeta
    

