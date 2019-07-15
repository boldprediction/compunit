import os
import cortex
import numpy as np

from hubs.config import Config
from analysis.individual import SubjectAnalysis
from serializer.html import HTMLImage


class FlatMap(SubjectAnalysis):

    def __call__(self, exp_name, subject, contrast, contrast_data):

        prefix = subject.name
        if np.sum(contrast_data.data < 0) == 0:
            prefix += '_pmap'
            volume = contrast_data
        else:
            volume = cortex.Volume(contrast_data.data,
                                   subject.name,
                                   subject.transform,
                                   **self.quickflat_args)

            volume.data[volume.data == 0] = np.nan

        file_name = '{0}_{1}_{2}_simple-flat-map.png'.format(prefix, exp_name, contrast.name)
        file_path = os.path.join(Config.image_dir, file_name)

        # Save flatmap
        try:
            cortex.quickflat.make_png(file_path,
                                      volume,
                                      with_colorbar=False,
                                      with_curvature=True,
                                      cvmin=-2,
                                      cvmax=2,
                                      **self.quickflat_args)
        except:
            cortex.quickflat.make_png(file_path,
                                      volume,
                                      with_colorbar=False,
                                      with_curvature=True,
                                      cvmin=-2,
                                      cvmax=2,
                                      recache=True,
                                      **self.quickflat_args)

        return HTMLImage('flat-map-analysis analysis', file_path)
