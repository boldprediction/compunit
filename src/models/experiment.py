from models.task import Task
from models.request import Request
from hubs.logger import Logger
from hubs.subjects import Subjects
from utils.parallelize import parallelize
from analysis.individual.webgl import WebGL
from analysis.individual.info import Info
from analysis.group.webglgroup import WebGLGroup
from analysis.result import AnalysisResult, AnalysisTextResult


class Experiment:

    def __call__(self, inputs):

        analyses = [Info(), WebGL()]
        group_analyses = [WebGLGroup()]
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
                Logger.debug(result.render())

            # execute group evaluation
            group_results = [ga(req.name, subjects, contrast, data) for ga in group_analyses]

            # render html
            # contrast info
            c1_names = str(contrast.condition1.names)
            c2_names = str(contrast.condition2.names)
            contrast_title = 'Contrast: {c1} - {c2}'.format(c1=c1_names, c2=c2_names)
            contrast_info = AnalysisTextResult('contrast-info', contrast_title)
            # group info
            group = AnalysisResult('group', group_results)
            # individuals
            individuals = AnalysisResult('individuals', results)

            output.append(AnalysisResult('contrast', [contrast_info, group, individuals]))

        return output
