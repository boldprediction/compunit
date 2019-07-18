import json
import numpy as np

from utils import clsname
from serializer import Serializable
from analysis.group import GroupAnalysis
from utils.cortex import make_static_light


class WebGLGroup(GroupAnalysis):

    def __call__(self,
                 exp_name,
                 subjects,
                 contrast,
                 contrast_results,
                 mean_volume,
                 mean_perm_volume,
                 **kwargs):

        if not contrast.do_perm:
            mean_volume.vmin = -1
            mean_volume.vmax = 2
            mean_volume.data[mean_volume.data == 0] = np.nan
            res_dict = {'contrast': contrast}
        else:
            mean_volume.vmin = -2
            mean_volume.vmax = 2
            mean_volume.data[mean_volume.data == 0] = np.nan
            res_dict = {'contrast': mean_volume, 'pmap': mean_perm_volume}

        # jsonstr = cortex.webgl.make_static_light(self.tmp_image_dir, res_dict)
        # result = {'images': {'__42f1b009d46afdc8': ['/static/simulate/data/__42f1b009d46afdc8_0.png']}, 'data': {'__42f1b009d46afdc8': {'name': '__42f1b009d46afdc8', 'min': -2.258884205267101, 'max': 2.543631070038396, 'raw': False, 'shape': [182, 218, 182], 'mosaic': [15, 11], 'subject': 'MNI'}}, 'views': [{'xfm': [[-1, 0, 0, 90, 0, 1, 0, 126, 0, 0, 1, 72, 0, 0, 0, 1]], 'name': 'contrast', 'vmin': [-2], 'state': None, 'cmap': ['RdBu_r'], 'attrs': {'priority': 1}, 'vmax': [2], 'data': ['__42f1b009d46afdc8'], 'desc': ''}]}

        result = make_static_light(res_dict)

        return Serializable({clsname(self): json.dumps(result)})
