import os
import numpy as np
import nibabel as ni

from utils import mni2vox
from constant import FSL_DIR


class Coordinate:
    """
    This class represents a point in the brain space.
    It has x,y,z coordinates and a score.
    """

    def __init__(self, xyz, name=None, zscore=None, size=8):

        self.name = name
        self.xyz = xyz
        self.zscore = zscore
        self.size = size

    def get_mni_roi_mask(self):
        """
        Given an MNI coordinate xyz (in mm) returns the ROI mask in MNI space.
        """
        radius = self.size

        # Load MNI template image
        default_template = os.path.join(FSL_DIR, "data", "standard", "MNI152_T1_1mm_brain.nii.gz")
        template = ni.load(default_template)

        # Get MNI affine transformation between mm-space and coord-space
        transformation = template.get_affine()

        # Convert MNI mm space to coordinate (voxel) space
        xyz = mni2vox(self.xyz, transformation)

        # Create an ROI mask
        # 0. Get MNI dims
        mni_dim = template.shape

        # 1. Draw a sphere around the vox_coord using the 'radius'
        MX, MY, MZ = np.ogrid[0:mni_dim[0], 0:mni_dim[1], 0:mni_dim[2]]
        roi = np.sqrt((MX-xyz[0])**2 + (MY-xyz[1])**2 + (MZ-xyz[2])**2) < radius

        return roi