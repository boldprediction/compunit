import os

from utils import read_json
from constant import CONF_DIR

class Subjects:

    class __SubjectSingleton__:

        def __init__(self, name, path, transform):
            info = read_json(os.path.join(CONF_DIR, "subject.json"))

