import json
import numpy as np

from utils import clsname
from serializer import Serializable
from utils.cortex import make_static_light
from analysis.individual import SubjectAnalysis


class WebGL(SubjectAnalysis):

    def __call__(self, exp_name, subject, contrast, contrast_data):

        contrast_data.vmax = 3
        contrast_data.vmin = -3

        contrast_data.data[subject.voxels_predicted == 0] = np.nan
        res_dict = {'contrast': contrast_data}

        if contrast.do_perm:
            res_dict['pmap'] = contrast_data.threshold_05
            res_dict['pmap'].data[subject.voxels_predicted == 0] = np.nan
            res_dict['pmap'].cmap = 'Blues'
            res_dict['pmap'].vmin = 0
            res_dict['pmap'].vmax = 1.25

        result = make_static_light(res_dict)

        return Serializable({clsname(self): json.dumps(result)})
