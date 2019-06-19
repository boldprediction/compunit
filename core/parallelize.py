import os
from multiprocessing import Pool

def parallelize(execs):

    res = []
    tokens = []
    pro_count = min(len(execs), os.cpu_count()-1)

    with Pool(processes = pro_count) as pool:

        for exec in execs:
            l = len(exec)
            func, param, kwparam = exec[0], exec[1] if l > 1 else [], exec[2] if l > 2 else {}
            token = pool.apply_async(func,param,kwparam)
            tokens.append(token)

        for t in tokens:
            res.append(t.get())

    return res