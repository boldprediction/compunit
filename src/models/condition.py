import numpy as np


class Condition:

    def __init__(self, words, model):
        self.words = [str.encode(w.strip()) for w in words]
        self.words_in_model = [w for w in self.words if w in model.vocab]

        if len(self.words_in_model) > 0:
            self.vector = np.vstack([model[w] for w in self.words_in_model]).mean(0)
        else:
            self.vector = np.zeros([1, model.ndim]).mean(0)
