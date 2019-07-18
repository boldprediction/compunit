import os

"""
This file aims to provide a collection of constants, so developers can 
import them at any time and won't worry how and when to initialize them 
"""
# source directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# root directory
ROOT_DIR = os.sep.join(SRC_DIR.split(os.sep)[:-1])

# configuration directory
CONF_DIR = os.path.join(ROOT_DIR, "conf")
if not os.path.exists(CONF_DIR):
    os.makedirs(CONF_DIR)

# logs directory
LOG_DIR = os.path.join(ROOT_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
# log out file
LOG_FILE = "compunit.log"

# data directory
DATA_DIR = os.path.join(ROOT_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# subjects directory
SUBJECTS_DIR = os.path.join(DATA_DIR, "subjects")
if not os.path.exists(SUBJECTS_DIR):
    os.makedirs(SUBJECTS_DIR)

# filestore directory, this folder is required by pycortex
FILE_STORE_DIR = os.path.join(DATA_DIR, "filestore")
if not os.path.exists(FILE_STORE_DIR):
    os.makedirs(FILE_STORE_DIR)

# semantic models directory
SEMANTIC_MODELS_DIR = os.path.join(DATA_DIR, "semanticmodels")
if not os.path.exists(SEMANTIC_MODELS_DIR):
    os.makedirs(SEMANTIC_MODELS_DIR)

# OUTPUTS_DIR = os.path.join(ROOT_DIR, "outputs")
OUTPUTS_DIR = '/Users/huangweiwei/studio/website/boldpredict/static/boldpredict/data'
if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR)
OUTPUTS_PREFIX = '/static/boldpredict/data/'

# FSL directory
FSL_DIR = os.getenv("FSLDIR")
if FSL_DIR is None:
    import warnings
    warnings.warn("Can't find FSLDIR environment variable, assuming default FSL location..")
    FSL_DIR = "/usr/local/fsl"
    os.environ["FSLDIR"] = FSL_DIR
    PATH = os.getenv("PATH")
    os.environ["PATH"] = PATH+":"+FSL_DIR+"/bin"

# FSL default template file path
FSL_DEFAULT_TEMPLATE = os.path.join(FSL_DIR, "data", "standard", "MNI152_T1_1mm_brain.nii.gz")

# MNI mask file path
MNI_MASK_FILE = os.path.join(DATA_DIR, "MNI_nan_mask.npy")


#coordinate space
MNI = 'mni'
TALAI = 'tala'

#stimuli type
WORD_LIST = "word_list"
SENTENCE = "sentence_list"
IMAGE = "image"

#model types
ENG1000 = "english1000"
WORD2VEC = "word2vec"
ELMo = "ELMo"
BERT = "BERT"
CNN = "CNN"
