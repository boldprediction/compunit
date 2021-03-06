import json
import time
from models.task import Task
from models.request import Request
from hubs.logger import Logger
from hubs.subjects import Subjects
from utils.parallelize import parallelize_tasks
from analysis.individual.webgl import WebGL
from analysis.group.webglgroup import WebGLGroup
from analysis.group.mean import Mean
from serializer import Serializable
from serializer.renders import Render
from utils.connections import update_contrast_result
from utils import clsname


class Experiment:
    """
    Experiment class defines the whole computation flow.
    It should be used as a function call.

    the abstract computation flow is described as the following steps:
    1. prepare analyses
    2. parse input as a request
    3. get the corresponding subjects
    4. for each contrast in the request:
        4.1. Create a task for each subject with the current contrast
        4.2. Execute all tasks parallely
        4.3. Use the collected data to perform group analyses
        4.4. Generate serializable result
    5. execute group analysis for the current contrast. About group analysis flow, see GroupAnalysis.py
    6. return all results
    """

    def __call__(self, inputs):

        # prepare analyses
        analyses = [WebGL()]
        group_analyses = [Mean(), WebGLGroup()]

        # render
        render = Render()

        # parse request
        Logger.info("Parsing request arguments ... [@performance]")
        begin_time = time.time()
        req = Request(**inputs)
        Logger.info("Parsing request arguments finished, time cost: "+str(time.time() - begin_time)+"s [@performance]")

        # get the corresponding subjects
        subjects = getattr(Subjects, req.semantic_model)

        # do computation and analyses for each contrast
        output = []
        for contrast in req.contrasts:
            # create tasks
            tasks = [Task(req.name, sub, contrast, analyses) for sub in subjects]

            # parallely compute individuals
            ret = parallelize_tasks(tasks)

            # run in sequence
            # import time
            # ret = []
            # t_begin = time.time()
            # for t in tasks:
            #     begin = time.time()
            #     ret.append(t.run())
            #     log_info = 'In sequence each task finishes in {0} seconds'.format(time.time() - begin)
            #     Logger.debug(log_info)
            # log_info = 'In sequence all the tasks finished in {0} seconds'.format(time.time() - t_begin)

            # collect results
            sub_res, data = zip(*ret)
            sub_res = {sub.name: {k: v for i in res for k, v in i.serialize().items()} for res, sub in zip(sub_res, subjects)}

            # execute group evaluation
            next_data = {'contrast_results': data}
            grp_res = {}
            for ga in group_analyses:
                begin_time = time.time()
                res = ga(req.name, subjects, contrast, **next_data)
                Logger.info("Executing group analysis {0} costs {1} s [@performance]".format(clsname(ga), str(time.time()-begin_time)))
                if isinstance(res, Serializable):
                    grp_res.update(res.serialize())
                elif isinstance(res, dict):
                    next_data.update(res)

            output.append(render.render(contrast, grp_res, sub_res))

        ret = json.dumps(output)
        Logger.debug(ret)
        update_contrast_result(ret)

        return ret
