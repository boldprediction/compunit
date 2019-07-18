from utils import recur_iter_attrs


class Serializable:
    """
    This class stands for a serializable object.
    """

    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, val)

    def serialize(self):
        return recur_iter_attrs(self.__dict__)

    def __str__(self):
        return self.serialize()
