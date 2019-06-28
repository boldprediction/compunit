import os

from utils import read_json
from constant import CONF_DIR


class __MetaConfig__(type):

    class __ConfigSingleton__:

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

    __singleton__ = None

    def __getattr__(cls, key):
        if not cls.__singleton__:
            cls.__singleton__ = __MetaConfig__.__ConfigSingleton__()
        config = cls.__singleton__.config
        return None if key not in config else config[key]


class Config(metaclass=__MetaConfig__):

    def __init__(self):
        raise RuntimeError("This class should not be instantiated!")
