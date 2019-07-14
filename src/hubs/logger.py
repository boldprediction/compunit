import os
import sys
import logging

from hubs.config import Config
from utils.singleton import MetaSingleton
from constant import SRC_DIR, LOG_DIR, LOG_FILE


DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_FORMAT = "[%(asctime)s | %(levelname)s | %(__call_func_line_number__)s] %(message)s"


class Logger(metaclass=MetaSingleton):

    class Singleton:
        def __init__(self):
            self.mappings = {}
            log_level = logging.INFO
            if Config.debug:
                log_level = logging.DEBUG

            logfile = os.path.join(LOG_DIR, LOG_FILE)
            logging.basicConfig(filename=logfile,
                                filemode='a',
                                level=log_level,
                                format=LOG_FORMAT,
                                datefmt=DATE_FORMAT)

    @classmethod
    def __get_logger__(cls,):

        # get calling stack
        caller = sys._getframe(2).f_code
        file = caller.co_filename
        file = file[len(SRC_DIR) + 1:]
        idstr = file+":" + str(caller.co_firstlineno) + ":" + str(caller.co_name) + "()"

        # if the corresponding logger has not been created yet
        if file not in cls.__singleton__.mappings:
            cls.__singleton__.mappings[file] = logging.getLogger(file)
            logger = cls.__singleton__.mappings[file]

            # if the system is running under debug mode
            # log info also need to be printed on the console
            if Config.debug:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
                handler.setFormatter(formatter)
                logger.addHandler(handler)

        logger = cls.__singleton__.mappings[file]

        return logger, idstr

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
