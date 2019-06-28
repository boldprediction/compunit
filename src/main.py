from hubs.config import Config
from hubs.logger import Logger


class Main:

    def start(self):
        print(Config.build_dir)
        Logger.debug("debug")
        Logger.info("info")


if __name__ == "__main__":
    Main().start()
