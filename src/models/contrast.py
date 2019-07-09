import numpy as np

from .coordinate import Coordinate


class Contrast:

    def __init__(self, name, condition1, condition2, coordinates, figures):

        # Given attributes

        # str
        self.name = name
        # Condition
        self.condition1 = condition1
        # Condition
        self.condition2 = condition2
        # list<Coordinate>
        self.coordinates = [Coordinate(**coord) for coord in coordinates]
        # list<str> paths of figures
        self.figures = figures

        # Generated attributes

        # stimuli names 1
        # 1d
        self.vector = self.vectorize(condition1, condition2)
        # bool
        self.double_sided = True
        if 'baseline' in condition2.names or np.all(condition2.matrix[0] == 0):
            self.double_sided = False

        # do bootstrap
        if not self.double_sided:
            words_cond1 = [w for w in []]
        else:
            pass

    def vectorize(self, condition1, condition2):
        # A contrast sometimes comprises a collection of conditions (e.g. check Davis2004).
        # We take the mean over the condition feature vectors for each contrast
        # FIXME: we can use nWords to normalize according to how many words we have in each sub condition
        vector1 = condition1.matrix.mean(0)
        vector2 = condition2.matrix.mean(0)
        # FIXME: why npp.zs? should we do it per subcondition?
        # vector = np.nan_to_num(npp.zs(vector1)) - np.nan_to_num(npp.zs(vector2))
        return vector1 - vector2


