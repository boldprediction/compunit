import time
from parallelize import parallelize

# def paral_func(subject,contrast,do_pmap,shared_list):
#     # paral_func using shared list
#     print("start one process")
#     begin = time.time()
#     res = subject.run(contrast, do_pmap)
#     print("[process calculation time cost] "+str(time.time()-begin))

#     print("start one process writing to shared list")
#     begin = time.time()
#     shared_list.append(res)
#     print("[process writing time cost] "+str(time.time()-begin))
#     print("finished one task")
#     return  0

def paral_func(subject,contrast,do_pmap,que):
    # paral_func using queue
    print("start one process")
    begin = time.time()
    res = subject.run(contrast, do_pmap)
    # print("result = ",res)
    print("[process calculation time cost] "+str(time.time()-begin))

    print("start one process writing to queue")
    begin = time.time()
    que.put((res[0],res[1]))
    print("[process writing time cost] "+str(time.time()-begin))
    print("finished one process")
    return  0

# def paral_func(subject,contrast,do_pmap,writer):
#     # paral_func using pipe
#     print("start one process")
#     begin = time.time()
#     res = subject.run(contrast, do_pmap)
#     # print("result = ",res)
#     print("[process calculation time cost] "+str(time.time()-begin))

#     print("start one process writing to pipe")
#     begin = time.time()
#     writer.send(res)
#     print("[process writing time cost] "+str(time.time()-begin))
#     print("finished one process")
#     writer.close()
#     return  0

# def paral_func(subject,contrast,do_pmap,shared_list,index):
#     # paral_func using  independent shared list
#     print("start one process")
#     begin = time.time()
#     shared_list[index] = subject.run(contrast, do_pmap)
#     print("[process calculation + writing time cost] "+str(time.time()-begin))
#     print("finished one task")
#     return  0

class SubjectGroup:

    def __init__(self, subjects, analyses, do_pmap = False):
        self.subjects = subjects
        self.analyses = analyses

    """
    
    """
    def aggregate(self, subres, contrast, do_pmap):
        applicables = None
        if isinstance(self.analyses[0], (list)):
            if do_pmap:
                applicables = self.analyses[1]
            else:
                applicables = self.analyses[0]
        else:
            applicables = self.analyses
            
        return [analyze(subres, self.subjects, contrast) for analyze in applicables]
    

    """
    combine contrasts from subjects somehow
    :param contrast: Contrast object
    :return: visualization object with everything
    """
    def run(self, contrast, do_pmap = False):
        
        # Make subject-wise results
        
        begin = time.time()

        executions = [(paral_func, [sub,contrast, do_pmap]) for sub in self.subjects]
        records = parallelize(executions)

        # records = [sub.run(contrast, do_pmap = do_pmap) for sub in self.subjects]

        print("[time cost] "+str(time.time()-begin))

        output, result = zip(*records)
        output = list(output)

        # Make group results
        groupres = self.aggregate(result, contrast, do_pmap)

        # Combine and return
        return [groupres] + output



## python3.8 3.9 supports a shared memory direct access 
## https://docs.python.org/3.8/library/multiprocessing.shared_memory.html