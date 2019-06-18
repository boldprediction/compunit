import time

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
        records = [sub.run(contrast, do_pmap = do_pmap) for sub in self.subjects]

        print("[time cost] "+str(time.time()-begin))

        output, result = zip(*records)
        output = list(output)

        # Make group results
        groupres = self.aggregate(result, contrast, do_pmap)

        # Combine and return
        return [groupres] + output