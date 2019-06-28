import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.sep.join(SRC_DIR.split(os.sep)[:-1])

CONF_DIR = os.path.join(ROOT_DIR, "conf")
if not os.path.exists(CONF_DIR):
    os.mkdir(CONF_DIR)

LOG_DIR = os.path.join(ROOT_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOG_FILE = "compunit.log"

