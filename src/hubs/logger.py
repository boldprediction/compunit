import os
import sys
import logging

from hubs.config import Config
from utils.singleton import MetaSingleton
from constant import SRC_DIR, LOG_DIR, LOG_FILE


DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_FORMAT = "[%(asctime)s | %(levelname)s | %(__call_func_line_number__)s] %(message)s"


class Logger(metaclass=MetaSingleton):
    """
    This is a logger class.
    Usage: Logger.debug(str)
    This logger will output messages into the given log file (constants.LOG_FILE)
    Also, this logger will print message into console if the current log info level is debug
    """

    class Singleton:
        def __init__(self):
            self.mappings = {}
            self.log_file = os.path.join(LOG_DIR, LOG_FILE)
            self.log_level = logging.DEBUG if Config.debug else logging.INFO

    @classmethod
    def __get_logger__(cls,):

        # get calling stack
        caller = sys._getframe(2).f_code
        file = caller.co_filename
        file = file[len(SRC_DIR) + 1:]
        id_str = file+":" + str(caller.co_firstlineno) + ":" + str(caller.co_name) + "()"

        # if the corresponding logger has not been created yet
        if file not in cls.__singleton__.mappings:
            cls.__singleton__.mappings[file] = logging.getLogger(file)
            logger = cls.__singleton__.mappings[file]
            level = cls.__singleton__.log_level
            formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

            # if the system is running under debug mode
            # log info also need to be printed on the console
            if Config.debug:
                sh = logging.StreamHandler()
                sh.setFormatter(formatter)
                sh.setLevel(level)
                logger.addHandler(sh)

            handler = logging.FileHandler(cls.__singleton__.log_file, mode='a')
            handler.setFormatter(formatter)
            handler.setLevel(level)
            logger.addHandler(handler)

        logger = cls.__singleton__.mappings[file]

        return logger, id_str

    @classmethod
    def debug(cls, log):
        logger, caller_info = Logger.__get_logger__()
        logger.debug(log, extra={"__call_func_line_number__": caller_info})

    @classmethod
    def info(cls, log):
        logger, caller_info = Logger.__get_logger__()
        logger.info(log, extra={"__call_func_line_number__": caller_info})

    @classmethod
    def error(cls, log):
        logger, caller_info = Logger.__get_logger__()
        logger.error(log, extra={"__call_func_line_number__": caller_info})
