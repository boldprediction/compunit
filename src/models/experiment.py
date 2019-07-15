import cortex

from models.task import Task
from models.request import Request
from hubs.logger import Logger
from hubs.subjects import Subjects
from utils.parallelize import parallelize
from analysis.individual.webgl import WebGL
from analysis.individual.info import Info
from analysis.group.webglgroup import WebGLGroup
from analysis.group.mean import Mean
from serializer import Serializable
from serializer.html import HTMLText, HTMLResult


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
        analyses = [Info(), WebGL()]
        group_analyses = [Mean(), WebGLGroup()]

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
            results, data = zip(*ret)
            for result in results:
                Logger.debug(result)

            # execute group evaluation
            next_data = {'contrast_results': data}
            group_results = []
            for ga in group_analyses:
                res = ga(req.name, subjects, contrast, **next_data)
                if isinstance(res, Serializable):
                    group_results.append(res)
                elif isinstance(res, dict):
                    next_data.update(res)

            # prepare
            # contrast info
            c1_names = str(contrast.condition1.names)
            c2_names = str(contrast.condition2.names)
            contrast_title = 'Contrast: {c1} - {c2}'.format(c1=c1_names, c2=c2_names)
            contrast_info = HTMLText('contrast-info', contrast_title)
            # group info
            group = HTMLResult('group', group_results)
            # individuals
            individuals = HTMLResult('individuals', results)

            output.append(HTMLResult('contrast', [contrast_info, group, individuals]))

        for o in output:
            Logger.debug(o)

        return output
