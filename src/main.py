import cortex
from cortex.options import config

from hubs.subjects import Subjects
from hubs.config import Config
from hubs.logger import Logger

import time


class Main:

    def start(self):
        # self.config_cortex()

        begin = time.time()
        array = Subjects.english1000
        print(time.time()- begin)


    # def config_cortex(self):
    #     print(config.get('basic', 'filestore'))


if __name__ == "__main__":
    Main().start()
