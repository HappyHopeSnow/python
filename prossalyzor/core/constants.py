
class Status:
    '''
    Processor execution result status.
    '''
    UNKNOWN = 0
    SUCCESS = 1
    FAILURE = 2
    

class Counter:
    '''
    Counter key.
    '''
    TOTAL = 0
    SUCCESS = 1
    FAILURE = 2
    
    
class Key:
    '''
    Common configuration key constants.
    '''
    JOB_CLASS                   = 'job.class'
    JOB_TASK_CLASSES            = 'job.task.classes'
    JOB_SCHEDULER_CLASS         = 'job.scheduler.class'
    JOB_EXECUTOR_POOL_CLASS     = 'job.executor.pool.class'
    JOB_POOL_SIZE               = 'job.pool.size'
    JOB_INPUT_CLASS             = 'job.input.class'
    JOB_OUTPUT_CLASS            = 'job.output.class'
    TASK_POOL_SIZE              = 'task.pool.size'
    TASK_EXECUTOR_POOL_CLASS    = 'task.executor.pool.class'
    

