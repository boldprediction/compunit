import json
from serializer import Serializable
from json import JSONEncoder


class JSONResult(Serializable,JSONEncoder):

    def __init__(self, data):
        self.data = data

    def serialize(self):
        # FIXME please recursively detect un-json-serializable object and deal with that
        string = json.dumps(self.data)
        return string
    
    def default(self):
        return self.data


