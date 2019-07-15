class Serializable:
    """
    This class stands for a serializable object.
    """

    def serialize(self):
        pass

    def __str__(self):
        return self.serialize()