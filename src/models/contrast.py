import numpy as np

from hubs.logger import Logger
from .stimulus import Stimulus
from .condition import Condition
from .coordinate import Coordinate


def vectorize(cond1, cond2, model):
    vector1 = cond1.to_vector_of_model(model)
    vector2 = cond2.to_vector_of_model(model)
    vector = vector1 - vector2
    return vector


class Contrast:

    def __init__(self, name, model, condition1, condition2, coordinates, do_perm, num_perm, figures):

        # Given attributes

        # str
        self.name = name
        # SemanticModel
        self.model = model
        # Condition
        self.condition1 = condition1
        # Condition
        self.condition2 = condition2
        # list<Coordinate>
        self.coordinates = [Coordinate(**coord) for coord in coordinates]
        # list<str> paths of figures
        self.figures = figures
        # bool
        self.do_perm = do_perm
        # int
        self.num_perm = num_perm


        # Generated attributes

        # 1d vector
        self.vector = vectorize(self.condition1, self.condition2, model)

        # bool
        self.double_sided = True
        if 'baseline' in condition2.names:
            self.double_sided = False

        if self.do_perm:
            if self.double_sided:
                self.permuted_vectors = self.double_side_permuted_vector()
            else:
                self.permuted_vectors = self.baseline_permuted_vector()
            log_info = 'generated {0} randomized vectors for contrast {1}'.format(self.num_perm, self.name)
            Logger.debug(log_info)

    def double_side_permuted_vector(self):
        words1 = [w for s in self.condition1.stimuli for w in s.words]
        words2 = [w for s in self.condition2.stimuli for w in s.words]
        words = words1 + words2
        words_len, len1, len2 = len(words), len(words1), len(words2)
        permuted_vectors = np.zeros((self.num_perm, self.model.ndim))

        for i in range(self.num_perm):
            permuted_words = np.random.permutation(words)
            cond1 = Condition([Stimulus(permuted_words[:len1])])
            cond2 = Condition([Stimulus(permuted_words[len1:])])
            permuted_vectors[i, :] = vectorize(cond1, cond2, self.model)

        return permuted_vectors

    def baseline_permuted_vector(self):

        words = [w for s in self.condition1.stimuli for w in s.words]
        permuted_vectors = np.zeros((self.num_perm, self.model.ndim))
        words_len = len(words)

        for i in range(self.num_perm):
            word_index = np.random.randint(words_len, size=words_len)
            random_words = [words[wi] for wi in word_index]
            cond1 = Condition([Stimulus(random_words)])
            cond2 = Condition.empty()
            permuted_vectors[i, :] = vectorize(cond1, cond2, self.model)

        return permuted_vectors
