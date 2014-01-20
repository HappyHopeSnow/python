from abc import ABCMeta, abstractmethod

class Endpoint:
    '''
    Endpoint abstraction.
    '''
    @abstractmethod
    def close(self):
        pass
    

class Server(Endpoint):
    '''
    Server abstraction.
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def listen(self):
        pass
    
    
class Client(Endpoint):
    '''
    Client abstraction.
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def connect(self):
        pass
    
    


