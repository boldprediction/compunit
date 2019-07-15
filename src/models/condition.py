import numpy as np

from models.stimulus import Stimulus


class Condition:
    """
    This model represents a collection of stimuli.
    It is actually a 2 dimension word matrix but has different length in each row
    """

    # stimuli: list<Stimulus>
    def __init__(self, stimuli):
        self.stimuli = stimuli
        self.names = [s.name for s in stimuli]

    def to_vector_of_model(self, model):
        return np.vstack([s.to_vector_of_model(model) for s in self.stimuli]).mean(0)

    @classmethod
    def empty(cls):
        return Condition([Stimulus.empty()])
