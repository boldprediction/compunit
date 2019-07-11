import numpy as np


class Stimulus:

    def __init__(self, words, name="", stimulus_type="word_list"):
        self.name = name
        self.type = stimulus_type
        self.words = words

    def to_vector_of_model(self, model):
        words_in_model = [w for w in self.words if w in model.vocab]
        if len(words_in_model) > 0:
            vector = np.vstack([model[w] for w in words_in_model]).mean(0)
        else:
            vector = np.zeros((1, model.ndim)).mean(0)
        return vector

    @classmethod
    def to_stimuli(cls, dic, model):

        stimuli = {}
        for k, attrs in dic.items():

            words_in_model = []
            words = attrs["value"].split(",")
            stimulus_type = attrs["type"] if "type" in attrs else "word_list"

            for word in words:
                w = str.encode(word.strip())
                if w in model.vocab:
                    words_in_model.append(w)

            stimuli[k] = Stimulus(words_in_model, k, stimulus_type)

        return stimuli

    @classmethod
    def empty(cls):
        return Stimulus([''])
