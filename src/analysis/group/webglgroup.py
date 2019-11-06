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
            res_dict = {'contrast': mean_volume}
        else:
            mean_volume.vmin = -2
            mean_volume.vmax = 2
            mean_volume.data[mean_volume.data == 0] = np.nan
            res_dict = {'contrast': mean_volume, 'pmap': mean_perm_volume}

        result = make_static_light(res_dict)

        return Serializable({clsname(self): json.dumps(result)})
