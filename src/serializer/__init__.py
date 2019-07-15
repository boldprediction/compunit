class Serializable:

    def serialize(self):
        pass

    def __str__(self):
        return self.serialize()