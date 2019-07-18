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


def clsname(c):
    """
    return the name of a class of the given object
    :param c:
    :return:
    """
    return c.__class__.__name__.lower()


def recur_iter_attrs(obj):
    """
    recursively iterate all attributes of an object to convert an object to
     a pure map(only contains built-in types)
    :param obj:
    :return:
    """

    if isinstance(obj, list) or isinstance(obj, tuple):
        res = []
        for i in obj:
            res.append(recur_iter_attrs(i))
        return res
    elif isinstance(obj, dict):
        dic = {}
        for k, v in obj.items():
            dic[k] = recur_iter_attrs(v)
        return dic
    elif obj is None\
        or isinstance(obj, int) \
        or isinstance(obj, float) \
        or isinstance(obj, complex) \
        or isinstance(obj, str) \
        or isinstance(obj, bool):
        return obj
    else:
        dic = {}
        for k, v in obj.__dict__.items():
            dic[k] = recur_iter_attrs(v)
        return dic