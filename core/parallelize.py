import os
# from multiprocessing import Pool, Manager,Process,Queue, Pipe
from queue import Queue
import threading
import time
import ray

# ray.init()

# @ray.remote
# def paral_func(subject,contrast,do_pmap):
#     # print("args = ", args)
#     #  = args[0],args[1],args[2]
#     # paral_func using ray
#     print("start one process")
#     begin = time.time()
#     res = subject.run(contrast, do_pmap)
#     print("[process calculation time cost] "+str(time.time()-begin))
#     print("finished one process")
#     return  res

# def parallelize(execs):
#     # parallelize using ray
#     results_ids = [] 
#     for exec in execs:
#         l = len(exec)
#         func, param, kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
#         # print("param = ", param)
#         results_ids.append(paral_func.remote(param[0],param[1],param[2]))
#     results = ray.get(results_ids)
#     print("results = ", results)
#     return results



# def pool_paral_func(param):
#     subject,contrast,do_pmap = param[0],param[1],param[2]
#     # paral_func using queue
#     print("start one process")
#     begin = time.time()
#     res = subject.run(contrast, do_pmap)
#     print("[process calculation time cost] "+str(time.time()-begin))
#     print("finished one process")
#     return res

# def pool_async_paral_func(subject,contrast,do_pmap):
#     # paral_func using queue
#     print("start one process")
#     begin = time.time()
#     res = subject.run(contrast, do_pmap)
#     print("[process calculation time cost] "+str(time.time()-begin))
#     print("finished one process")
#     return res

# def parallelize(execs):

#     res = []
#     tokens = []
#     pro_count = min(len(execs), os.cpu_count()-1)

#     # shared memory
#     manager = Manager()
#     shared_list = manager.list()

#     with Pool(processes = pro_count) as pool:

#         for exec in execs:
#             l = len(exec)
#             func, param, kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
#             param.append(shared_list)
#             token = pool.apply_async(func,param,kwparam)
#             tokens.append(token)

#         for t in tokens:
#             res.append(t.get())

#     return res

# def parallelize(execs):
#     # parallelize using manager managed shared memory 

#     begin = time.time()
#     print("start parallelizing")

#     res = []
#     tokens = []
#     pro_count = min(len(execs), os.cpu_count()-1)

#     # shared memory
#     manager = Manager()
#     l_exec = len(execs)
#     shared_list = manager.list()
#     p_list= []
#     for i in range(l_exec):
#         exec = execs[i]
#         l = len(exec)
#         func,param , kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
#         param.append(shared_list)
#         p = Process(target=func, args=param)
#         p.start()
    
#     while len(shared_list) < 3:
#         time.sleep(1)
    
#     print("[parallelizing time cost] "+str(time.time()-begin))

#     print("result = ", shared_list)
#     return shared_list



# def parallelize(execs):
#     # parallelize using Pool

#     begin = time.time()
#     print("start parallelizing")

#     res = []
#     params_list = []

#     for exec in execs:
#         l = len(exec)
#         func, param , kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
#         params_list.append(param)

#     with Pool(3) as pool:
#         res.append(pool.map(pool_paral_func,params_list))
    
#     print("[parallelizing time cost] "+str(time.time()-begin))
#     print("res = ", res)
#     return res

# def parallelize(execs):
#     # parallelize using Pool async
#     res = []
#     tokens = []
#     pro_count = min(len(execs), os.cpu_count()-1)

#     begin = time.time()
#     print("start parallelizing")

#     with Pool(processes = pro_count) as pool:

#         for exec in execs:
#             l = len(exec)
#             func, param, kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
#             token = pool.apply_async(pool_async_paral_func,param,kwparam)
#             tokens.append(token)

#         for t in tokens:
#             res.append(t.get())
    
#     print("[parallelizing time cost] "+str(time.time()-begin))
#     print("res = ", res)

#     return res


# def parallelize(execs):
#     # parallel using pipe -  This is the fastest !!!

#     begin = time.time()
#     print("start parallelizing")

#     res = []
#     tokens = []

#     l_exec = len(execs)
#     p_list= []

#     readers = []

#     for exec in execs:
#         r, w = Pipe(duplex=False)
#         readers.append(r)
#         l = len(exec)
#         func,param , kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
#         param.append(w)
#         p = Process(target=func, args=param)
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
#     # parallelize using q = Queue()
#     # cost 31 seconds.

#     p_begin = time.time()
#     print("start parallelizing")

#     res = []
#     tokens = []
#     pro_count = min(len(execs), os.cpu_count()-1)

#     # shared memory
#     l_exec = len(execs)
#     p_list= []
#     q = Queue()
#     for exec in execs:
#         l = len(exec)
#         func,param , kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
#         param.append(q)
#         p = Process(target=func, args=param)
#         p.start()
    
#     print("start read ")

#     for i in range(l_exec):
#         print("start read")
#         begin = time.time()
#         q_res = q.get(True)
#         print("finish get i =  ", i , str(time.time()-begin))
#         res.append(q_res)
    
#     print("[parallelizing time cost] "+str(time.time()-p_begin))
#     return res


def parallelize(execs):
    # parallelize using threading

    p_begin = time.time()
    print("start parallelizing")

    res = []
    tokens = []
    pro_count = min(len(execs), os.cpu_count()-1)

    # shared memory
    l_exec = len(execs)
    p_list= []
    q = Queue()
    for exec in execs:
        l = len(exec)
        func,param , kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
        param.append(q)
        p = threading.Thread(target=func, args=param)
        # p = Process(target=func, args=param)
        p_list.append(p)
    
    for p in p_list:
        p.start()

    for p in p_list:
        p.join()

    for i in range(l_exec):
        print("start read")
        begin = time.time()
        q_res = q.get(True)
        print("finish get i =  ", i , str(time.time()-begin))
        res.append(q_res)
    
    print("[parallelizing time cost] "+str(time.time()-p_begin))
    return res