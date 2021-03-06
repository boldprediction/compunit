import os

from utils import read_json
from constant import CONF_DIR
from utils.singleton import MetaSingleton


class Config(metaclass=MetaSingleton):
    """
    This class loads configurations from conf/config.json.
    if a top-level configuration key ends with '_dir', then this class
    will test whether the directory exists. If it does not exist, this class
    will create it recursively

    For all configuration, it can be referred like Config.xxx
    """
    class Singleton:

        def __init__(self):
            """
            Checks if the config.json file exists and loads this.
            Otherwise loads the config_default.json file
            """
            secret_config_file_path = os.path.join(CONF_DIR, "secret_config.json")
            conf_file_path = os.path.join(CONF_DIR, "config.json")
            if os.path.exists(conf_file_path):
                print("User config file for directories is used.")
            else:
                print("Default config file for directories is used. If you want\
                    to use your own directory structure create a config.json file\
                    under directory " + CONF_DIR)
                conf_file_path = os.path.join(CONF_DIR, "config_default.json")

            self.config = read_json(conf_file_path)
            self.secret_config = read_json(secret_config_file_path)

        def __getattr__(self, key):
            if key not in self.config and key not in self.secret_config:
                raise AttributeError
            else:
                item = None
                if key in self.config:
                    item = self.config[key]
                    if key.endswith("_dir") and not os.path.exists(item):
                        os.makedirs(item)
                else:
                    item = self.secret_config[key]
                    if key.endswith("_dir") and not os.path.exists(item):
                        os.makedirs(item)

                return item
