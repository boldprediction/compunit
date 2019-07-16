import os
from concurrent.futures import ThreadPoolExecutor
import time

from hubs.logger import Logger

def task_run(task):
    log_info = "task begin" 
    Logger.debug(log_info)
    t_begin = time.time()
    ret = task.run()
    log_info = 'In parallel each task finishes in {0} seconds'.format(time.time() - t_begin)
    Logger.debug(log_info)
    return ret
    
# def task_run(task,writer):
#     # for using pipe
#     log_info = "task begin" 
#     Logger.debug(log_info)
#     t_begin = time.time()
#     ret = task.run()
#     print("calculation time = ",time.time() - t_begin )
#     writer.send(ret)
#     writer.close()
#     log_info = 'In parallel each task finishes in {0} seconds'.format(time.time() - t_begin)
#     Logger.debug(log_info)
#     return 0

def parallelize_tasks(tasks):

    cpu_count = min(len(tasks), os.cpu_count() - 1)
    print("cpu_count  = ", cpu_count)
    
    with ThreadPoolExecutor(max_workers=cpu_count) as executor:
        begin = time.time()
        results = executor.map(task_run, tasks)
        print("task results = ",results)
        results_list = list(results)

        log_info = 'In parallel all the tasks finished in {0} seconds'.format(time.time() - begin)
        Logger.debug(log_info)

        return results_list

    return [] 


# from multiprocessing import Pool
# def parallelize_tasks(tasks):
#     # using pool

#     cpu_count = min(len(tasks), os.cpu_count() - 1)
    
#     with Pool(processes = cpu_count) as pool:
#         begin = time.time()
#         results = pool.map(task_run, tasks)
#         results_list = list(results)

#         log_info = 'In parallel all the tasks finished in {0} seconds'.format(time.time() - begin)
#         Logger.debug(log_info)

#         return results_list

#     return [] 

# from multiprocessing import Pool, Manager,Process,Queue, Pipe
# def parallelize_tasks(tasks):
#     # parallel using pipe -  This is the fastest !!!

#     begin = time.time()
#     print("start parallelizing")

#     res = []
#     tokens = []

#     l_exec = len(tasks)
#     p_list= []

#     readers = []

#     for task in tasks:
#         r, w = Pipe(duplex=False)
#         readers.append(r)
#         param = []
#         param.append(task)
#         param.append(w)
#         p = Process(target=task_run, args=param)
#         p.start()

#     while readers:
#         for r in readers:
#             try:
#                 msg = r.recv()
#                 res.append(msg)
#             except EOFError:
#                 readers.remove(r)
#             else:
#                 print(msg)
#                 readers.remove(r)

#     print("[parallelizing time cost] "+str(time.time()-begin))

#     return res

# def parallelize(execs):
#     """
#     Parallelize computations by using multi-threads
#     :param execs:
#     :return:
#     """
#
#     p_begin = time.time()
#     print("start parallelizing")
#
#     res = []
#     cpu_count = min(len(execs), os.cpu_count() - 1)
#
#     l_exec = len(execs)
#     p_list = []
#     q = Queue()
#     for k in range(1):
#         for exec in execs:
#             l = len(exec)
#             func, param, kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
#             if k == 0:
#                 param.append(q)
#             # print("param = ", param)
#             p = threading.Thread(target=func, args=param)
#             p_list.append(p)
#
#     for p in p_list:
#         p.start()
#
#     for p in p_list:
#         p.join()
#
#     for k in range(1):
#         for i in range(l_exec):
#             print("start read")
#             begin = time.time()
#             q_res = q.get(True)
#             print("finish get i =  ", i, str(time.time() - begin))
#             res.append(q_res)
#
#     print("[parallelizing time cost] " + str(time.time() - p_begin))
#     return res