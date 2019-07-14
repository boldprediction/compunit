import os
from concurrent.futures import ThreadPoolExecutor

from hubs.logger import Logger


def parallelize(execs):

    callbacks = []
    cpu_count = min(len(execs), os.cpu_count() - 1)
    with ThreadPoolExecutor(max_workers=cpu_count) as executor:
        for execution in execs:
            l = len(execution)
            func, args, kwargs = execution[0], execution[1] if l > 1 else [], execution[2] if l > 2 else {}
            future = executor.submit(func, *args, **kwargs)
            callbacks.append(future)

    results = []
    for callback in callbacks:
        try:
            res = callback.result()
            results.append(res)
        except Exception as exc:
            Logger.error(str(exc))

    return results


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