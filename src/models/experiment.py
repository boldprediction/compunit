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

    def __call__(self, inputs):

        analyses = [Info(), WebGL()]
        group_analyses = [Mean(), WebGLGroup()]
        req = Request(**inputs)
        subjects = getattr(Subjects, req.semantic_model)

        output = []

        for contrast in req.contrasts:
            # parallely compute individuals
            tasks = [Task(req.name, sub, contrast, analyses) for sub in subjects]
            # ret = parallelize([(t.run,) for t in tasks])
            ret = [t.run() for t in tasks]
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

            # render html
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
