import cortex
import numpy as np

from analysis.individual import SubjectAnalysis
from analysis.result import AnalysisTextResult


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

        json_str = cortex.webgl.make_static_ligtht(self.tmp_image_dir, res_dict)

        return AnalysisTextResult('webgl-analysis analysis', json_str)
