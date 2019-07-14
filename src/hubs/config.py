import os

from utils import read_json
from constant import CONF_DIR
from utils.singleton import MetaSingleton


class Config(metaclass=MetaSingleton):

    class Singleton:

        def __init__(self):
            """
            Checks if the config.json file exists and loads this.
            Otherwise loads the config_default.json file
            """
            conf_file_path = os.path.join(CONF_DIR, "config.json")
            if os.path.exists(conf_file_path):
                print("User config file for directories is used.")
            else:
                print("Default config file for directories is used. If you want\
                    to use your own directory structure create a config.json file\
                    under directory " + CONF_DIR)
                conf_file_path = os.path.join(CONF_DIR, "config_default.json")

            self.config = read_json(conf_file_path)

        def __getattr__(self, key):
            if key not in self.config:
                raise AttributeError
            else:
                item = self.config[key]
                if key.endswith("_dir") and not os.path.exists(item):
                    os.makedirs(item)

                return item
