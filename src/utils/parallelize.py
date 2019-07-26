import os
import time
from concurrent.futures import ThreadPoolExecutor

from hubs.logger import Logger


def task_run(task):
    Logger.debug("task begin")
    t_begin = time.time()
    ret = task.run()
    Logger.info('In parallel each task finishes in {0} seconds'.format(time.time() - t_begin) + " [@performance]")
    return ret


def parallelize_tasks(tasks):
    cpu_count = min(len(tasks), os.cpu_count() - 1)    
    with ThreadPoolExecutor(max_workers=cpu_count) as executor:
        begin = time.time()
        results = executor.map(task_run, tasks)
        results_list = list(results)
        log_info = 'In parallel all the tasks finished in {0} seconds [@performance]'.format(time.time() - begin)
        Logger.info(log_info)
        
        return results_list

