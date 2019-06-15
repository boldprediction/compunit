import os
import cortex
import numpy as np

class SubjectAnalysis:
    def __call__(self, contrast_data):
        pass

class EmptyAnalysis(SubjectAnalysis):
    def __init__(self):
        pass

    def __call__(self, contrast_data):
        return str(contrast_data)

class TotalEffectSize(SubjectAnalysis):
    def __init__(self):
        pass

    def __call__(self, contrast_data):
        total_effect_size = np.sqrt((contrast_data.data ** 2).mean())
        return "Total effect size (RMS): %0.3f" % total_effect_size

class Flatmap(SubjectAnalysis):
    def __init__(self, output_root, path, show_total_effect_size=True, **quickflat_args):
        self.path = path
        self.output_root = output_root
        self.quickflat_args = quickflat_args
        self.show_total_effect_size = show_total_effect_size

    def __call__(self, contrast_data):
        if hasattr(contrast_data, 'ref_to_subject'):
            prefix = contrast_data.ref_to_subject
        else:
            prefix = 'group'

        if np.sum(contrast_data.data < 0) == 0:
            prefix += '_pmap'
            tmp_volume = contrast_data
        else:
            tmp_volume = cortex.Volume(contrast_data.data,
                                        contrast_data.subject,
                                        contrast_data.xfmname,
                                        ** self.quickflat_args)
            tmp_volume.data[tmp_volume.data == 0] = np.nan

        filename = '{0}_{1}_{2}_simpleFlatmap.png'.format(prefix, contrast_data.contrast.experiment.name, contrast_data.contrast.contrast_name)
        filename = os.path.join(self.path, filename)
        print("[Flatmap.__call__ : filename] "+filename)

        path = os.path.join(self.output_root, filename)
        try:
            cortex.quickflat.make_png(path, tmp_volume, with_colorbar = False,
                                      with_curvature = True, cvmin = -2, cvmax = 2, **self.quickflat_args)
        except:
            cortex.quickflat.make_png(path, tmp_volume, with_colorbar = False,
                        with_curvature = True, cvmin = -2, cvmax = 2, recache = True, 
                        **self.quickflat_args)

        return contrast_data