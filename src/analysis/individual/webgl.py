import json
import numpy as np

from utils import clsname
from serializer import Serializable
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

        # json_str = cortex.webgl.make_static_ligtht(self.tmp_image_dir, res_dict)
        result = {'images': {'__ba48df7dedd3c7bd': ['/static/simulate/data/__ba48df7dedd3c7bd_0.png']}, 'data': {'__ba48df7dedd3c7bd': {'name': '__ba48df7dedd3c7bd', 'min': -4.926231504192491, 'max': 4.383638110956946, 'raw': False, 'shape': [32, 100, 100], 'mosaic': [6, 6], 'subject': 'Afs'}}, 'views': [{'xfm': [[-0.4458947402193688, 0.01804466454210354, 0.012276020652923205, 51.013559958162446, -0.016672237337077685, -0.4436775580803444, 0.0465907540298967, 64.24405861218081, 0.007638548740702911, 0.024990693780280637, 0.24071647511978078, 19.70224960671398, 0, 0, 0, 1]], 'name': 'contrast', 'vmin': [-3], 'state': None, 'cmap': ['RdBu_r'], 'attrs': {'priority': 1}, 'vmax': [3], 'data': ['__ba48df7dedd3c7bd'], 'desc': ''}]}
        return Serializable({clsname(self): json.dumps(result)})
