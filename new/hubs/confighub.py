import os
from ..utils import read_json
from ..constant import BASE_DIR


class ConfigHub:

    class ConfigSingleton:

        def __init__(self):
            """
            Checks if the config_user.json file exists and loads this. Otherwise
            loads the config_default.json file.
            """
            if os.path.exists(os.path.join(BASE_DIR, dir, "config_user.json")):
                print("User config file for directories is used.")
                config = read_json("config_user.json", filepath=dir)
            else:
                print("Default config file for directories is used. If you want\
                    to use your own directory structure create a config_user.json file\
                    under ./jsons.")
                config = read_json("config_default.json")

            return config



    def __init__(self):
        pass