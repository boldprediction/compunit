import numpy as np
from SemanticModel import SemanticModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FSLDIR = os.getenv("FSLDIR")
if FSLDIR is None:
    import warnings
    warnings.warn("Can't find FSLDIR environment variable, assuming default FSL location..")
    #FSLDIR = "/usr/local/fsl-5.0.10"
    FSLDIR = "/usr/local/fsl"
    os.environ["FSLDIR"] = FSLDIR
    PATH = os.getenv("PATH")
    os.environ["PATH"] = PATH+":"+FSLDIR+"/bin"

def load_config(dir = 'json'):
    # FIXME: I actually would like to have the caller method name
    # and not the caller module name. But didn't find it yet.
    caller_object = sys._getframe(1).f_code
    caller_name = caller_object.co_filename
    print("load_config is called by {}".format(caller_name))

    """
    Checks if the config_user.json file exists and loads this. Otherwise
    loads the config_default.json file.
    """
    if os.path.exists(os.path.join(BASE_DIR,json_dir,"config_user.json")):
        print("User config file for directories is used.")
        config = read_json("config_user.json", filepath = dir)
    else:
        print("Default config file for directories is used. If you want\
        to use your own directory structure create a config_user.json file\
        under ./jsons.")
        config = read_json("config_default.json")
    
    return config

def load_model(type, dir='jsons'):
    
    config = load_config(dir)
    model_dir = config["model_dir"][model_type]

    if model_type == 'english1000':
        print('\n Loaded english1000! \n')
        return SemanticModel.load(os.path.join(model_dir, "english1000sm.hf5"))
    else:
        raise ValueError('Unknown model type: %s' % self.model_type)


"""
Given an MNI coordinate (mm-space) and the affine transformation of the 
image (nifti_image.get_affine()) this function returns the coordinates in 
voxel space.
"""
def mni2vox(mni_coord, transform):
    return np.array(mni_coord+[1]).dot(np.linalg.inv(transform).T)[:3]