from hubs.subjects import Subjects
from hubs.config import Config
from hubs.logger import Logger

import time

from hubs.semanticmodels import SemanticModels


class Main:

    def start(self):
        Logger.debug("trying to start")
        print(Config.semanticmodels)
        print(SemanticModels.english1000)
        begin = time.time()
        print(Subjects.english1000)
        print(time.time()-begin)




if __name__ == "__main__":
    Main().start()
