import nipy
import cortex
import numpy as np

from hubs.logger import Logger
from analysis.group import GroupAnalysis
from constant import MNI_MASK_FILE, FSL_DEFAULT_TEMPLATE


class Mean(GroupAnalysis):

    def __init__(self, smooth=None, thresh=0.01, do_1pct=False, mask_pred=False, recompute_mask=False):
        self.smooth = smooth
        self.threshold = thresh
        self.do_1pct = do_1pct
        self.mask_pred = mask_pred
        self.recomputed_mask = recompute_mask
        if not self.recomputed_mask:
            self.nan_mask = np.load(MNI_MASK_FILE)

    def __call__(self, exp_name, subjects, contrast, contrast_results):

        # Prepare volumes
        volumes = {}
        if self.mask_pred:
            for s, cr in zip(subjects, contrast_results):
                mask = s.voxels_predicted
                mask = cortex.Volume(mask, s.name, s.transform)
                s.data[mask.data == True] = -1
                if contrast.do_perm:
                    #FIXME which threshold?
                    cr.thresholded_contrast.data[mask.data==True] = -1
                    volumes[cr.subject] = s

        if contrast.do_perm:
            if not self.mask_pred:
                volumes = {con_res.subject: con_res.threshold_05 for con_res in contrast_results}
            else:
                pass
        else:
            volumes = {con_res.subject: con_res for con_res in contrast_results}

        for v in volumes.values():
            v.data = np.nan_to_num(v.data)

        # Re-compute mask
        if self.recomputed_mask:
            # FIXME should it be s.predicted_mask_mni ?
            # s2 = [s.predicted_mask_MNI for s in subjects]
            s2 = [s.predicted_mask_mni for s in subjects]
            self.nan_mask = np.mean(np.stack(s2), axis=0)
            self.nan_mask = self.nan_mask >= 3 / 8.0
            np.save(MNI_MASK_FILE, self.nan_mask)

        mni_volumes = [cortex.mni.transform_to_mni(volumes[s.name], s.func_to_mni).get_data().T for s in subjects]

        # Smooth
        if self.smooth is not None:
            Logger.debug("Smoothing with %f mm kernel.." % self.smooth)
            atlasim = nipy.load_image(FSL_DEFAULT_TEMPLATE)
            smoother = nipy.kernel_smooth.LinearFilter(atlasim.coordmap, atlasim.shape, self.smooth)

            new_mni_volumes = []
            for ml in mni_volumes:
                # Create nipy-style Image from volume
                ml_img = nipy.core.image.Image(ml.T, atlasim.coordmap)
                # Pass it through smoother
                sm_ml_img = smoother.smooth(ml_img)
                # Store the result
                new_mni_volumes.append(sm_ml_img.get_data().T)
            mni_volumes = new_mni_volumes

        # Mean values
        group_mean = np.mean(np.stack(mni_volumes), axis=0)
        group_mean[self.nan_mask == False] = np.nan
        un_nan = np.isnan(group_mean) * self.nan_mask
        group_mean[un_nan] = 0

        max_v_volume = 1 if contrast.do_perm or self.do_1pct else 2

        if self.do_1pct:
            th = np.percentile(group_mean[group_mean != 0], 90)
            group_mean = group_mean >= th

        mean_volume = cortex.Volume(group_mean,
                                    'MNI',
                                    'atlas',
                                    vmin=-max_v_volume,
                                    vmax=max_v_volume)

        sub_volumes = [cortex.Volume(vol,
                                     'MNI',
                                     'atlas',
                                     vmin=-np.abs(vol).max(),
                                     vmax=np.abs(vol).max())
                       for vol in mni_volumes]

        for sub, vol in zip(subjects, sub_volumes):
            vol.data[sub.predicted_mask_mni == False] = np.nan

        return mean_volume, sub_volumes
