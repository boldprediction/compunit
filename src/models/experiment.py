from .contrast import Contrast
from .condition import Condition
from hubs.semanticmodels import SemanticModels


class Experiment:

    def __init__(self,
                 DOI='',
                 title='',
                 nperm=1000,
                 authors=[],
                 stimuli={},
                 contrasts={},
                 do_perm=False,
                 coordinate_space='MNI',
                 semantic_model="english1000",
                 **extra_infos):

        # FIXME: the experiment name should be generated automatically
        self.name = 'random'

        # given properties
        self.DOI = DOI
        self.title = title
        self.nperm = nperm
        self.authors = authors
        self.stimuli = stimuli
        self.permutation = do_perm
        self.coordinate_space = coordinate_space
        self.semantic_model = semantic_model
        self.extra_infos = extra_infos

        # generated properties
        self.model = getattr(SemanticModels, semantic_model)
        self.contrasts = [Contrast(name, **pairs) for name, pairs in sorted(contrasts.items())]
        self.conditions = {k: Condition(words["value"].split(","), self.model) for k, words in stimuli.items()}

    def run(self):
        print("running")
