from .coordinate import Coordinate


class Contrast:

    def __init__(self, name, condition1, condition2, coordinates, figures):
        # str
        self.name = name
        # list<str>
        self.condition1 = condition1
        # list<str>
        self.condition2 = condition2
        # list<Coordinate>
        self.coordinates = [Coordinate(**coord) for coord in coordinates]
        # list<str> paths of figures
        self.figures = figures

