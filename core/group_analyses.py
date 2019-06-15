import nipy
import cortex
import numpy as np
from cortex.mni import transform_to_mni
from nipy.algorithms import kernel_smooth
from subject_analyses import SubjectAnalysis

class GroupAnalysis:
    def __init__(self):
        return super().__init__()

class ContrastVolume(cortex.Volume):
    def __init__(self, 
                data, 
                subject_name, 
                xfm_name, 
                vmin, vmax, 
                contrast, 
                isPmap=False,
                 **extra):
       cortex.Volume.__init__(self,data,
                              subject_name,
                              xfm_name,
                              vmin = vmin,
                              vmax = vmax,
                              **extra)
       self.contrast = contrast
       self.isPmap = isPmap
       if self.isPmap:
            self.vmin = 0
            self.vmax = 1
            self.cmap = 'Blues'

class Mean:

    def __init__(self, 
                visualizer, 
                smooth = None,
                pmap = False,
                thresh = 0.001,
                do_1pct = False,
                mask_pred = False,
                recompute_mask = False):

        self.visualizer = visualizer
        self.smooth = smooth
        self.pmap = pmap
        self.thresh = thresh
        self.do_1pct = do_1pct
        self.mask_pred = mask_pred
        self.recompute_mask = recompute_mask
        
        if not self.recompute_mask:
            self.nan_mask = np.load('MNI_nan_mask.npy')

    def __call__(self,
                subjects_result,
                subjcets,
                contrast):

        outputs = []
        mean_volume, sub_volumes = self.get_group_mean(subjects_result, subjects, contrast)
        for vis in self.visualizer:
            if isinstance(vis, SubjectAnalysis):
                outputs.append(vis(mean_volume))
            elif isinstance(vis, GroupAnalysis):
                outputs.append(vis(mean_volume, sub_volumes, contrast))
            else:
                raise ValueError('Unkown visualization type: %s' % repr(vis))

        return outputs

    def get_group_mean(self, subjects_result, subjects, contrast):
        subject_volumes = {}
        if self.mask_pred:
            for s in subjects_result:
                mask = s.ref_to_subject._voxels_predicted
                mask = cortex.Volume(mask, s.ref_to_subject.pycortex_surface, s.ref_to_subject.pycortex_transform)
                s.data[mask.data == True] = -1
                if self.pmap:
                    s.thresholded_contrast.data[mask.data == True] = -1
                    subject_volumes[s.subject] = s
        if self.pmap:
            if not self.mask_pred:
                subject_volumes = {subres.subject : subres.thresholded_contrast_05 for subres in subjects_result}
        
        else:
            subject_volumes = {subres.subject : subres for subres in subjects_result}
        
        for s in subject_volumes.values():
            s.data = np.nan_to_num(s.data)

        if self.recompute_mask:
            s2 = [s.predicted_mask_MNI for s in subjects]
            self.nan_mask = np.mean(np.stack(s2), axis = 0)
            self.nan_mask = self.nan_mask >= 3/8.0
            np.save("MNI_nan_mask.npy", self.nan_mask)


        subject_mni_volumes = [transform_to_mni(subject_volumes[subject.pycortex_surface],
                                                subject.func_to_mni, use_flirt=use_flirt).get_data().T for subject in subjects]
        

        if self.smooth is not None:
            print("Smoothing with %f mm kernel.." % self.smooth)
            # Do some smoothing! self.smooth is FWHM of smoother
            atlasim = nipy.load_image(default_template)
            smoother = kernel_smooth.LinearFilter(atlasim.coordmap, 
                                                  atlasim.shape,
                                                  self.smooth)

            unsm_subject_mni_volumes = subject_mni_volumes

            subject_mni_volumes = []
            for svol in unsm_subject_mni_volumes:
                # Create nipy-style Image from volume
                svol_im = nipy.core.image.Image(svol.T, atlasim.coordmap)
                # Pass it through smoother
                sm_svol_im = smoother.smooth(svol_im)
                # Store the result
                subject_mni_volumes.append(sm_svol_im.get_data().T)

        group_mean = np.mean(np.stack(subject_mni_volumes),axis =0)

        group_mean[self.nan_mask == False] = np.nan
        un_nan = np.isnan(group_mean) * self.nan_mask
        group_mean[un_nan] = 0

        if self.pmap or self.do_1pct:
            max_v_volume = 1
        else:
            max_v_volume = 2

        if self.do_1pct:
            th = np.percentile(group_mean[group_mean!=0],90)
            group_mean = group_mean>=th

        mean_volume = ContrastVolume(group_mean, 'MNI', 'atlas',
                                    vmin=-max_v_volume,
                                    vmax= max_v_volume,
                                    contrast = contrast,
                                    isPmap = self.pmap)


        sub_volumes = [ContrastVolume(vol, 'MNI', 'atlas',
                                     vmin=-np.abs(vol).max(),
                                     vmax=np.abs(vol).max(),
                                     contrast = contrast)
                       for vol in subject_mni_volumes]

        for idx,v in enumerate(sub_volumes):  # mask the subject volumes for prediction
            v.data[subjects[idx].predicted_mask_mni == False] = np.nan

        return mean_volume, sub_volumes

class Mean_two(Mean):

    def __init__(self, 
                visualizer, 
                smooth=None, 
                pmap = False, 
                thresh = 0.01, 
                do_1pct=False, 
                mask_pred = False,
                recompute_mask = False):

        Mean.__init__(self, 
                visualizer = visualizer, 
                smooth = smooth, 
                pmap = pmap, 
                thresh = thresh, 
                do_1pct = do_1pct,
		        mask_pred = mask_pred, 
                recompute_mask = recompute_mask)

    def __call__(self, subjects_result, subjects, contrast):
        self.pmap = False
        mean_volume, sub_volumes = self.get_group_mean(subjects_result, subjects, contrast)
        self.pmap = True
        mean_volume_pmap, sub_volumes_pmap = self.get_group_mean(subjects_result, subjects, contrast)
        outputs = []
        for vis in self.visualizers:
            if isinstance(vis, SubjectAnalysis):
                # It's a subject analysis, just give it the mean
                outputs.append(vis([mean_volume, mean_volume_pmap, sub_volumes, sub_volumes_pmap, contrast]))

            elif isinstance(vis, GroupAnalysis):
                # It's a group analysis, give it mean and individual volumes & contrast
                outputs.append(vis(mean_volume_pmap, sub_volumes_pmap, contrast))  ### FIXEME I REPLACED SUB_VOLUMES WITH SUBJECT RESULTS

            else:
                raise ValueError('Unknown visualization type: %s' % repr(vis))

        return outputs