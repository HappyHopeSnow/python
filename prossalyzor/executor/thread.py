from concurrent.futures.thread import ThreadPoolExecutor

from prossalyzor.core.common import PoolExecutor
from prossalyzor.core.constants import Key


class ThreadedPoolExecutor(PoolExecutor):
    '''
    Pooled executor implementation based on a wrapped
    ThreadPoolExecutor object.
    '''
    def __init__(self, context, max_workers=1):
        super(ThreadedPoolExecutor, self).__init__(context)
        self._pool = ThreadPoolExecutor(max_workers)
    
    def execute(self, task):
        self._pool.submit(task.processor)