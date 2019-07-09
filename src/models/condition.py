import numpy as np


class Condition:

    # stimuli: list<Stimulus>
    def __init__(self, stimuli):
        self.names = [s.name for s in stimuli]
        self.matrix = np.vstack([s.vector for s in stimuli])