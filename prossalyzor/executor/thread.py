from concurrent.futures.thread import ThreadPoolExecutor

from prossalyzor.core.common import PoolExecutor


class ThreadedPoolExecutor(PoolExecutor):
    '''
    Pooled executor implementation based on a wrapped
    ThreadPoolExecutor object.
    '''
    def __init__(self, context, max_workers=1):
        super(ThreadedPoolExecutor, self).__init__(context)
        self._pool = ThreadPoolExecutor()
    
    def execute(self, task, callback):
        pass