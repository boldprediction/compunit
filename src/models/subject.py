import cortex
import tables


class Subject:
    """
    This class stands for a subject(brain). Brain data will be loaded from file
    """

    def __init__(self, name, transform, path):

        # basic attributes
        self.name = name
        self.transform = transform
        self.func_to_mni = cortex.db.get_mnixfm(name, transform)

        # attributes from file
        with tables.open_file(path) as tf:

            # voxels_predicted
            self.pred_score = tf.root.corr.read()
            threshold = 0.05
            self.voxels_predicted = self.pred_score > threshold

            # weights
            self.weights = tf.root.udwt.read()
            self.weights[:, self.voxels_predicted is False] = 0

        #predicted_mask_mni
        tmp = cortex.Volume(self.voxels_predicted.astype("float"), name, transform)
        self.predicted_mask_mni = cortex.mni.transform_to_mni(tmp, self.func_to_mni).get_data().T
        self.predicted_mask_mni = (self.predicted_mask_mni > 0) * 1.0


