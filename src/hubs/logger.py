import os
import sys
import logging

from constant import SRC_DIR, LOG_DIR, LOG_FILE
from hubs.config import Config

DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_FORMAT = "[%(asctime)s | %(levelname)s | %(__call_func_line_number__)s] %(message)s"


class Logger:

    class __LoggerMapping__:
        def __init__(self, is_debug):
            self.mappings = {}
            log_level = logging.INFO
            if is_debug is not None and is_debug:
                log_level = logging.DEBUG

            logfile = os.path.join(LOG_DIR, LOG_FILE)
            logging.basicConfig(filename=logfile,
                                filemode='a',
                                level=log_level,
                                format=LOG_FORMAT,
                                datefmt=DATE_FORMAT)

    is_debug = False
    logger_mapping = None

    @classmethod
    def __get_logger__(cls,):

        # instantiate singleton
        if not cls.logger_mapping:
            is_debug = Config.debug
            cls.logger_mapping = Logger.__LoggerMapping__(is_debug)

        # get calling stack
        caller = sys._getframe(2).f_code
        file = caller.co_filename
        file = file[len(SRC_DIR) + 1:]
        idstr = file+":" + str(caller.co_firstlineno) + ":" + str(caller.co_name) + "()"

        # if the corresponding logger has not been created yet
        if file not in cls.logger_mapping.mappings:
            cls.logger_mapping.mappings[file] = logging.getLogger(file)
            logger = cls.logger_mapping.mappings[file]

            # if the system is running under debug mode
            # log info also need to be printed on the console
            if is_debug is not None and is_debug:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
                handler.setFormatter(formatter)
                logger.addHandler(handler)

        logger = cls.logger_mapping.mappings[file]

        return logger, idstr

    @classmethod
    def debug(cls, template, *args):
        logger, caller_info = Logger.__get_logger__()
        logger.debug(template, extra={"__call_func_line_number__":caller_info})

    @classmethod
    def info(cls, template, *args):
        logger, caller_info = Logger.__get_logger__()
        logger.info(template, extra={"__call_func_line_number__":caller_info})