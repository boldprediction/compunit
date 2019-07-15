import cortex
import numpy as np

from analysis.group import GroupAnalysis
from analysis.group.mean import Mean

from analysis.result import AnalysisTextResult


class WebGLGroup(GroupAnalysis):

    def __call__(self, exp_name, subjects, contrast, contrast_results):

        mean = Mean()
        mean_volume = mean(exp_name, subjects, contrast, contrast_results)

        if not contrast.do_perm:
            mean_volume.vmin = -1
            mean_volume.vmax = 2
            mean_volume.data[mean_volume.data == 0] = np.nan
            res_dict = {'contrast': contrast}
        else:
            not_perm = mean_volume[0]
            perm = mean_volume[1]
            not_perm.vmin = -2
            not_perm.vmax = 2
            not_perm.data[not_perm.data == 0] = np.nan
            res_dict = {'contrast': not_perm, 'pmap': perm}

        # jsonstr = cortex.webgl.make_static_light(self.tmp_image_dir, res_dict)
        jsonstr = '{"images":{"__42f1b009d46afdc8":["/static/simulate/data/__42f1b009d46afdc8_0.png"]},"data":{"__42f1b009d46afdc8":{"name":"__42f1b009d46afdc8","min":-2.258884205267101,"max":2.543631070038396,"raw":false,"shape":[182,218,182],"mosaic":[15,11],"subject":"MNI"}},"views":[{"xfm":[[-1,0,0,90,0,1,0,126,0,0,1,72,0,0,0,1]],"name":"contrast","vmin":[-2],"state":null,"cmap":["RdBu_r"],"attrs":{"priority":1},"vmax":[2],"data":["__42f1b009d46afdc8"],"desc":""}]}'

        return AnalysisTextResult('mean-webglgroup-analysis analysis', jsonstr)
