import os
import tables
import cortex
import numpy as np

use_flirt = False
## Rescale -- make each column have unit variance
rescale = lambda v: v/v.std(0)
rescale.__doc__ = """Rescales each column of [v] to have unit variance."""

class Subject:

    def __init__(self,
                name,
                pycortex_surface,
                xfm,
                models,
                model_type,
                model_dir,
                analyses,
                **extra_info):
        
        self.name = name
        self.model_path = os.path.join(model_dir[model_type], models[model_type])
        # These things have to be str and not unicode for pycortex C compatibility
        self.pycortex_surface = str(pycortex_surface)
        self.pycortex_transform = str(xfm)

        print("xfm = "+self.pycortex_transform)
        print("surface = "+self.pycortex_surface)

        self.analyses = analyses
        self.extra_info = extra_info
        self.func_to_mni = cortex.db.get_mnixfm(self.pycortex_surface, self.pycortex_transform)

        with tables.open_file(self.model_path) as tf:
            self.weights = tf.root.udwt.read()
            self.pred_score = tf.root.corr.read()
            threshold = 0.05
            self.voxels_predicted = self.pred_score > threshold
            self.weights[:, self.voxels_predicted == False] = 0

        fvoxels = self.voxels_predicted.astype("float")
        tmp = cortex.Volume(fvoxels, self.pycortex_surface, self.pycortex_transform)

        # @Leila, is that okay to remove use_flirt?
        print("##################",self.func_to_mni,"#####################")
        self.predicted_mask_mni = cortex.mni.transform_to_mni(tmp, self.func_to_mni).get_data().T
        self.predicted_mask_mni = (self.predicted_mask_mni > 0) * 1.0
        

    """
    run all contrasts through model
    :param contrast: Contrast object
    :return: data volume containing the map
    """
    def run(self, contrast, do_pmap = False):
        # Create contrast Volume
        data = self.weights.T.dot(contrast.vector)
        data[self.voxels_predicted] = rescale(data[self.voxels_predicted])
        data[self.voxels_predicted == False] = np.nan
        contrast_data = ContrastData(
            np.nan_to_num(data),
            self.pycortex_surface,
            self.pycortex_transform,
            vmin = -np.abs(np.nan_to_num(data)).max(),
            vmax = np.abs(np.nan_to_num(data)).max(),
            contrast = contrast,
            func_to_mni = self.func_to_mni,
            ref_to_subject = self
        )
        # Run analyses
        if isinstance(self.analyses[0], (list)):
            if do_pmap:
                results = [analysis(contrast_data) for analysis in self.analyses[1]]
            else:
                results = [analysis(contrast_data) for analysis in self.analyses[0]]
        else:
            results = [analysis(contrast_data) for analysis in self.analyses]
        # return [self.make_output(results),contrast_data]
        return [results, contrast_data]


def FDR(vector, q, do_correction = False):
    original_shape = vector.shape
    vector = vector.flatten()
    N = vector.shape[0]
    sorted_vector = sorted(vector)
    C = np.sum([1.0/i for i in range(N)]) if do_correction else 1.0
    thresh = 0
    #a=b
    for i in range(N-1, 0, -1):
        if sorted_vector[i]<= (i*1.0)/N*q/C:
            thresh = sorted_vector[i]
            break
    thresh_vector = vector<=thresh
    thresh_vector = thresh_vector.reshape(original_shape)
    thresh_vector = thresh_vector*1.0
    print("FDR threshold is : {}, {} voxels rejected".format(thresh, thresh_vector.sum()))
    return thresh_vector, thresh



class ContrastData(cortex.Volume):

    def __init__(self, 
                data, 
                subject_name,
                xfmname, 
                vmin, 
                vmax,
                contrast,
                func_to_mni,
                ref_to_subject,
                cmap='RdBu_r'):
        super().__init__(data, subject_name, xfmname, vmin=vmin, vmax=vmax, cmap=cmap)
        self.contrast = contrast
        self.func_to_mni = func_to_mni
        self.ref_to_subject = ref_to_subject

        #permuted_contrast_pval
        p_contrast_vecs = np.dot(self.contrast.permuted_vectors,self.ref_to_subject.weights)
        contrast_vect = np.dot(self.contrast.vector, self.ref_to_subject.weights)
        if self.contrast.double_sided:
            counts = (contrast_vect <= p_contrast_vecs).mean(0)
            # can't have pval=0
            counts[counts==0] = 1.0/p_contrast_vecs.shape[0] 
            # these are areas with no predictions
            counts[self.ref_to_subject.voxels_predicted == False] = 0
            p_map = counts 
        else:
            counts = (np.zeros_like(contrast_vect) >= p_contrast_vecs).mean(0)
            # can't have pval=0
            counts[counts==0] = 1.0/p_contrast_vecs.shape[0] 
            # these are areas with no predictions
            counts[self.ref_to_subject.voxels_predicted == False] = 0 
            p_map = counts

        self.permuted_contrast_pval = cortex.Volume(p_map,self.ref_to_subject.pycortex_surface, self.ref_to_subject.pycortex_transform, vmin=0,vmax=1)
        
        # thresholded_contrast_05
        thresholded_contrast_05 = self.permuted_contrast_pval.data
        thresholded_contrast_05[thresholded_contrast_05 > 0] = FDR(thresholded_contrast_05[thresholded_contrast_05>0], 0.05, do_correction=False)[0]
        self.thresholded_contrast_05 = cortex.Volume(thresholded_contrast_05,self.ref_to_subject.pycortex_surface, self.ref_to_subject.pycortex_transform, vmin=-0.5,vmax=0.5)

        # thresholded_contrast_05_mni
        self.thresholded_contrast_05_mni = cortex.mni.transform_to_mni(self.thresholded_contrast_05, self.func_to_mni).get_data().T

        # thresholded_contrast_01
        thresholded_contrast_01 = self.permuted_contrast_pval.data
        thresholded_contrast_01[thresholded_contrast_01>0] = FDR(thresholded_contrast_01[thresholded_contrast_01>0],0.01, do_correction=False)[0]
        self.thresholded_contrast_01 = cortex.Volume(thresholded_contrast_01, self.ref_to_subject.pycortex_surface, self.ref_to_subject.pycortex_transform, vmin=-0.5,vmax=0.5)

        # thresholded_contrast_01_mni
        self.thresholded_contrast_01_mni = cortex.mni.transform_to_mni(self.thresholded_contrast_01, self.func_to_mni).get_data().T
