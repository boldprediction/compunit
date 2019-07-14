from models.stimulus import Stimulus
from models.condition import Condition
from models.contrast import Contrast
from hubs.semanticmodels import SemanticModels


class Request:

    def __init__(self,
                 DOI='',
                 name='',
                 title='',
                 authors=[],
                 stimuli={},
                 contrasts={},
                 coordinate_space='MNI',
                 semantic_model="english1000",
                 **extra_infos):

        # FIXME: the experiment name should be generated automatically if it is null
        self.name = name

        # given properties
        self.DOI = DOI
        self.title = title
        self.authors = authors
        self.semantic_model = semantic_model
        self.coordinate_space = coordinate_space
        self.extra_infos = extra_infos

        # generated properties
        self.model = getattr(SemanticModels, semantic_model)
        self.stimuli = Stimulus.to_stimuli(stimuli, self.model)
        self.contrasts = []
        for name, attrs in sorted(contrasts.items()):
            cond1 = Condition([self.stimuli[s1] for s1 in attrs.pop("condition1")])
            cond2 = Condition([self.stimuli[s2] for s2 in attrs.pop("condition2")])
            c = Contrast(name, self.model, cond1, cond2, **attrs)
            self.contrasts.append(c)
