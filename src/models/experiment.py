from .contrast import Contrast
from .stimulus import Stimulus
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
        self.stimuli = {k: Stimulus(k, words["value"].split(","), self.model) for k, words in stimuli.items()}
        self.contrasts = []
        for name, attrs in sorted(contrasts.items()):
            cond1 = Condition([self.stimuli[s1] for s1 in attrs["condition1"]])
            cond2 = Condition([self.stimuli[s2] for s2 in attrs["condition2"]])
            c = Contrast(name, cond1, cond2, **attrs)
            self.contrasts.append(c)

    def run(self):
        print("running")
