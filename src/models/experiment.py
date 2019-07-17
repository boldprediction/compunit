import cortex

from models.task import Task
from models.request import Request
from hubs.logger import Logger
from hubs.subjects import Subjects
from utils.parallelize import parallelize
from analysis.individual.webgl import WebGL
from analysis.group.webglgroup import WebGLGroup
from analysis.group.mean import Mean
from serializer import Serializable
from serializer.renders.json import JSONRender


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
        render = JSONRender()

        # parse request
        req = Request(**inputs)

        # get the corresponding subjects
        subjects = getattr(Subjects, req.semantic_model)

        # do computation and analyses for each contrast
        output = []
        for contrast in req.contrasts:
            # create tasks
            tasks = [Task(req.name, sub, contrast, analyses) for sub in subjects]

            # parallely compute individuals
            # ret = parallelize([(t.run,) for t in tasks])
            ret = [t.run() for t in tasks]

            # collect results
            individual_results, data = zip(*ret)

            # execute group evaluation
            next_data = {'contrast_results': data}
            group_results = []
            for ga in group_analyses:
                res = ga(req.name, subjects, contrast, **next_data)
                if isinstance(res, Serializable):
                    group_results.append(res)
                elif isinstance(res, dict):
                    next_data.update(res)

            output.append(render.render(contrast, group_results, individual_results))

        for o in output:
            Logger.debug(o)

        return output
