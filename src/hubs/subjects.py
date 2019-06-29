import os

from utils import read_json
from constant import CONF_DIR, SUBJECTS_DIR
from collections import defaultdict
from models.subject import Subject
from utils.singleton import MetaSingleton


class Subjects(metaclass=MetaSingleton):

    class Singleton:
        def __init__(self):
            self.infos = read_json(os.path.join(CONF_DIR, "subject.json"))
            self.models = defaultdict(list)
            self.subjects = defaultdict(list)
            for info in self.infos:
                name = info["name"]
                transform = info["transform"]
                models = info["models"]
                for model, file in models.items():
                    self.models[model].append({"name": name, "transform": transform, "file": file})

        def __getattr__(self, key):
            if key == 'infos':
                return self.infos
            elif key == "models":
                return self.models
            elif key not in self.models:
                raise AttributeError()
            else:
                if key not in self.subjects:
                    for subject in self.models[key]:
                        self.subjects[key].append(self.__load_subject__(key, subject))
                return self.subjects[key]

        def __load_subject__(self, model_type, subject):
            name = subject["name"]
            file = subject["file"]
            transform = subject["transform"]
            path = os.path.join(SUBJECTS_DIR, model_type, file)
            return Subject(name, transform, path)
