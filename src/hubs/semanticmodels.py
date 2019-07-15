import os

from hubs.config import Config
from constant import SEMANTIC_MODELS_DIR
from utils.singleton import MetaSingleton
from models.semanticmodel import SemanticModel


class SemanticModels(metaclass=MetaSingleton):
    """
    This class is actually a semantic model center.
    Usage: SemanticModels.english1000 will return a SemanticModel object
    initialized with english1000 data file
    """

    class Singleton:

        def __init__(self):
            self.infos = Config.semanticmodels
            self.models = {}

        def __getattr__(self, key):
            if key == "infos":
                return self.infos
            elif key == "models":
                return self.models
            else:
                # no corresponding semantic model
                if key not in self.infos:
                    raise AttributeError("No corresponding semantic model: "+key)

                # load model
                if key not in self.models:
                    path = os.path.join(SEMANTIC_MODELS_DIR, self.infos[key])
                    self.models[key] = SemanticModel.load(path)

                return self.models[key]

