import cortex
from cortex.options import config

from hubs.subjects import Subjects
from hubs.config import Config
from hubs.logger import Logger

import time

from hubs.semanticmodels import SemanticModels


class Main:

    def start(self):
        # subjects = Subjects.english1000
        print(SemanticModels.english1000)




if __name__ == "__main__":
    Main().start()
