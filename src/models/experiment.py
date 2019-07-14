from models.task import Task
from models.request import Request
from hubs.logger import Logger
from hubs.subjects import Subjects
from utils.parallelize import parallelize
from analysis.individual.webgl import WebGL


class Experiment:

    def __init__(self, inputs):
        analyses = [WebGL()]
        req = Request(**inputs)
        subjects = getattr(Subjects, req.semantic_model)

        for contrast in req.contrasts:
            tasks = [Task(req.name, sub, contrast, analyses) for sub in subjects]
            # ret = parallelize([(t.run,) for t in tasks])
            ret = [t.run() for t in tasks]
            results, data = zip(*ret)
            for result in results:
                Logger.debug(result.render())

    def run(self):
        print("running")
