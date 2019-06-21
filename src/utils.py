import json


def read_json(filepath):
    """
    Returns a json files content.
    """
    return json.loads(open(filepath).read())


