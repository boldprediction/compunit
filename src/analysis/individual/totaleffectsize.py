import numpy as np
from analysis.individual import SubjectAnalysis
from serializer.html import HTMLText


class TotalEffectSize(SubjectAnalysis):

    def __call__(self, exp_name, subject, contrast, contrast_data):
        total_effect_size = np.sqrt((contrast_data.data ** 2).mean())
        html = "Total effect size (RMS): %0.3f" % total_effect_size
        return HTMLText('total-effect-size-analysis analysis', html)
