import numpy as np


class Stimulus:

    def __init__(self, name, words, model, stimulus_type="word_list"):

        self.name = name
        self.type = stimulus_type
        self.words = [str.encode(w.strip()) for w in words]
        self.words_in_model = [w for w in self.words if w in model.vocab]

        if len(self.words_in_model) > 0:
            self.vector = np.vstack([model[w] for w in self.words_in_model]).mean(0)
        else:
            self.vector = np.zeros([1, model.ndim]).mean(0)
