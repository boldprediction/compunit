import numpy as np
from utils import clsname
from utils.npp import rescale
from models.contrastdata import ContrastData



class Task:
    """
    This class aims to execute the simplest computation: a computation with only one
    subject under only one contrast.
    1. compute required data
    2. compute permuted data if necessary
    3. construct analyzable data for the following analyses
    4. execute analyses and collect the result
    """

    def __init__(self, exp_name, subject, contrast, analyses):

        self.experiment_name = exp_name
        self.subject = subject
        self.contrast = contrast
        self.analyses = analyses

    def run(self):

        exp_name = self.experiment_name
        subject = self.subject
        contrast = self.contrast
        analyses = self.analyses

        # computation
        data, vmin, vmax = self.compute()
        permuted_data = self.compute_with_permutation()

        # construct analyzable object
        contrast_data = ContrastData(data,
                                     permuted_data,
                                     subject.name,
                                     subject.transform,
                                     subject.func_to_mni,
                                     vmin=vmin,
                                     vmax=vmax)

        # execute analyses
        results = [a(exp_name, subject, contrast, contrast_data) for a in analyses]

        return results, contrast_data

    def compute(self):
        # data preparation
        data = self.subject.weights.T.dot(self.contrast.vector)
        data[self.subject.voxels_predicted] = rescale(data[self.subject.voxels_predicted])
        data[self.subject.voxels_predicted == False] = np.nan

        nan_to_num_data = np.nan_to_num(data)
        vmin = -np.abs(data).max()
        vmax = np.abs(data).max()

        return nan_to_num_data, vmin, vmax

    def compute_with_permutation(self):
        # prepare permutation data
        permuted_data = None
        if self.contrast.do_perm:
            permuted_matrix = np.dot(self.contrast.permuted_vectors, self.subject.weights)
            contrast_vec = np.dot(self.contrast.vector, self.subject.weights)

            if self.contrast.double_sided:
                counts = (contrast_vec <= permuted_matrix).mean(0)
            else:
                counts = (np.zeros_like(contrast_vec) >= permuted_matrix).mean(0)

            # can't have pval=0
            counts[counts == 0] = 1.0 / permuted_matrix.shape[0]
            # these are areas with no predictions
            counts[self.subject.voxels_predicted == False] = 0
            permuted_data = counts

        return permuted_data
