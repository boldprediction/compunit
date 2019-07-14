import cortex
import numpy as np
from hubs.logger import Logger
from cortex.mni import transform_to_mni


def FDR(vector, q, do_correction = False):
    original_shape = vector.shape
    vector = vector.flatten()
    N = vector.shape[0]
    sorted_vector = sorted(vector)
    if do_correction:
        C = np.sum([1.0/i for i in range(N)])
    else:
        C = 1.0
    thresh = 0
    #a=b
    for i in range(N-1, 0, -1):
        if sorted_vector[i]<= (i*1.0)/N*q/C:
            thresh = sorted_vector[i]
            break
    thresh_vector = vector <= thresh
    thresh_vector = thresh_vector.reshape(original_shape)
    thresh_vector = thresh_vector * 1.0

    log_info = "FDR threshold is : {}, {} voxels rejected".format(thresh, thresh_vector.sum())
    Logger.debug(log_info)
    return thresh_vector, thresh


class ContrastData(cortex.Volume):

    def __init__(self,
                 data,
                 permuted_data,
                 name,
                 transform,
                 func_to_mni,
                 vmin,
                 vmax,
                 cmap='RdBu_r'):

        cortex.Volume.__init__(self,
                               data,
                               name,
                               transform,
                               vmin=vmin,
                               vmax=vmax,
                               cmap=cmap)

        self.permuted_contrast_pval = None
        self.threshold_05 = None
        self.threshold_01 = None
        self.threshold_05_mni = None
        self.threshold_01_mni = None

        if permuted_data is not None:

            # permuted contrast pycortex value
            self.permuted_contrast_pval = permuted_data

            # threshold 05
            threshold_05 = permuted_data
            threshold_05[threshold_05 > 0] = FDR(threshold_05[threshold_05 > 0], 0.05, do_correction=False)[0]
            self.threshold_05 = cortex.Volume(threshold_05, name, transform, vmin=-0.5, vmax=0.5)

            # threshold 05 mni
            self.threshold_05_mni = transform_to_mni(self.threshold_05, func_to_mni).get_data().T

            # threshold 01
            threshold_01 = permuted_data
            threshold_01[threshold_01 > 0] = FDR(threshold_01[threshold_01 > 0], 0.01, do_correction=False)[0]
            self.threshold_01 = cortex.Volume(threshold_01, name, transform, vmin=-0.5, vmax=0.5)

            # threshold 01 mni
            self.threshold_01_mni = transform_to_mni(self.threshold_01, func_to_mni).get_data().T
