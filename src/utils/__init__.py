import json
import numpy as np


def read_json(filepath):
    """
    Returns a json files content.
    """
    return json.loads(open(filepath).read())


def mni2vox(mni_coord, transform):

    """
    Given an MNI coordinate (mm-space) and the affine transformation of the
    image (nifti_image.get_affine()) this function returns the coordinates in
    voxel space.

    """
    return np.array(mni_coord+[1]).dot(np.linalg.inv(transform).T)[:3]
