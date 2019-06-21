import os
from utils import read_json
from constant import CONF_DIR


class ConfigHub:

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

    def __init__(self):
        cls = self.__class__
        if not cls.__singleton__:
            cls.__singleton__ = ConfigHub.__ConfigSingleton__()

    def __getattr__(self, name):
        return getattr(self.__singleton__, name)
