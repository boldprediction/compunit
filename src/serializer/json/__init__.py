import json
from serializer import Serializable


class JSONResult(Serializable):

    def __init__(self, data):
        self.data = data

    def serialize(self):
        # FIXME please recursively detect un-json-serializable object and deal with that
        string = json.dumps(self.data)
        return string
    
    def __str__(self):
        return str(self.data)


