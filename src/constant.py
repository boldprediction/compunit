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

FILE_STORE_DIR = os.path.join(DATA_DIR, "filestore")
if not os.path.exists(FILE_STORE_DIR):
    os.mkdir(FILE_STORE_DIR)

SEMANTIC_MODELS_DIR = os.path.join(DATA_DIR, "semanticmodels")
if not os.path.exists(SEMANTIC_MODELS_DIR):
    os.mkdir(SEMANTIC_MODELS_DIR)

FSL_DIR = os.getenv("FSLDIR")
if FSL_DIR is None:
    import warnings
    warnings.warn("Can't find FSLDIR environment variable, assuming default FSL location..")
    FSL_DIR = "/usr/local/fsl"
    os.environ["FSLDIR"] = FSL_DIR
    PATH = os.getenv("PATH")
    os.environ["PATH"] = PATH+":"+FSL_DIR+"/bin"
