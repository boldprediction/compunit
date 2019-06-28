import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.sep.join(SRC_DIR.split(os.sep)[:-1])

CONF_DIR = os.path.join(ROOT_DIR, "conf")
if not os.path.exists(CONF_DIR):
    os.mkdir(CONF_DIR)

LOG_FILE = "compunit.log"
LOG_DIR = os.path.join(ROOT_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

DATA_DIR = os.path.join(ROOT_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

SUBJECTS_DIR = os.path.join(DATA_DIR, "subjects")
if not os.path.exists(SUBJECTS_DIR):
    os.mkdir(SUBJECTS_DIR)

FILESTORE_DIR = os.path.join(DATA_DIR, "filestore")
if not os.path.exists(FILESTORE_DIR):
    os.mkdir(FILESTORE_DIR)

SEMANTICMODELS_DIR = os.path.join(DATA_DIR, "semanticmodels")
if not os.path.exists(SEMANTICMODELS_DIR):
    os.mkdir(SEMANTICMODELS_DIR)