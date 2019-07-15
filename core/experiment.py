import os
import time
import numpy as np
import nibabel as ni
from utils import load_model, mni2vox, FSLDIR

class Experiment:
    def __init__(
                self,
                model_holder = '',
                name = '',
                stimuli = [],
                contrasts = [],
                tasks = [],
                coordinate_space = 'MNI',
                DOI = '',
                image_dir = '',
                model_type = 'english1000',
                nperm = 1000,
                **extra_info):
        
        self.name = name
        self.DOI = DOI
        self.extra_info = extra_info
        self.model_type = model_type
        self.nperm = nperm
        self.tasks = tasks
        self.model_holder = model_holder
        self.model = self.model_holder.get_model(self.model_type)
        self.coordinate_space = coordinate_space
        self.conditions = self.make_conditions(stimuli)
        self.contrasts = self.make_contrasts(contrasts, image_dir)

    def make_conditions(self, stimuli):
        
        conditions = {}
        for con, word_list in stimuli.items():
            if self.name == 'KRNS':
                words = word_list['value'].split(' ')
                words = [w.replace('.','').replace(',','').lower() for w in words]
                conditions[con] = Condition(words, self.model)
            else:
                conditions[con] = Condition(word_list['value'].split(', '), self.model)
        
        return conditions

    """
    Make contrast structure.
    """
    def make_contrasts(self, contrasts_dict, image_dir):
        contrasts = {}
        for con, info in sorted(contrasts_dict.items()):
            cont_1 = info['condition1']
            cont_2 = info['condition2']
            coordi = info['coordinates']
            figures = info['figures']
            contrasts[con] = Contrast(cont_1, cont_2, coordi, figures, self, image_dir, contrast_name = con)
        return contrasts

    def run(self, subject_group, do_pmap = False):
        # Make results for each contrast
        results = []
        sorted_contrasts = sorted(self.contrasts.keys())
        for contrast in sorted_contrasts:
            t = time.time()
            print("{0} of experiment {1} ...  ".format(contrast, self.name)),
            con = self.contrasts[contrast]
            conres = con.run(subject_group, do_pmap = do_pmap)
            results.append(conres)
            print("completed in {0} seconds".format(time.time()-t))
        # print("results = ", results)
        return results


class ModelHolder:
    def __init__(self, directory='./jsons'):
        self.models = {}
        self.directory = directory
    
    def get_model(self, model_type):
        if model_type not in self.models:
            self.models[model_type] = load_model(model_type, self.directory)
        return self.models[model_type]

class Condition:
    def __init__(self, words, model):
        self.words = [w.encode() if type(w) == str else w for w in words]
        self.words_in_model = [w for w in self.words if w in model.vocab]
        if len(self.words_in_model) > 0:
            self.vector = np.vstack([model[w] for w in self.words_in_model]).mean(0)
        else:
            self.vector = np.zeros((1, model.ndim)).mean(0)


class Contrast:
    def __init__(self, cond_1, cond_2, coords, images,
                experi, path, contrast_name='tmp',):
        condition1 = [experi.conditions[c] for c in cond_1]
        condition2 = [experi.conditions[c] for c in cond_2]
        self.vector = self.make_contrast_vector(condition1, condition2)
        self.coordinates = [Coordinates(**c) for c in coords]
        self.condition_names = [cond_1,cond_2]
        
        flag = np.all(experi.conditions[cond_2[0]].vector == 0)
        if self.condition_names[1][0] == 'baseline' or flag:
            self.double_sided = False
        else:
            self.double_sided = True
        
        self.contrast_name = contrast_name
        # self.experiment = experi
        self.path = path

        if not self.double_sided:
            # do bootstrap
            words_cond1 = [w for w in [experi.conditions[cond].words_in_model for cond in self.condition_names[0]]]
            words_cond1 = [w for s in words_cond1 for w in s]
            nwords1 = len(words_cond1)
            self.permuted_vectors = np.zeros([experi.nperm, experi.model.ndim])
            for i in range(experi.nperm):
                pw = np.random.randint(nwords1, size = nwords1)
                tmpcond1 = Condition([words_cond1[iw] for iw in pw],experi)
                tmpcond2 = Condition([''],experi)
                self.permuted_vectors[i,:] = self.make_contrast_vector([tmpcond1],[tmpcond2])
        else:
            # do permutation test
            words_cond1 = [w for w in [experi.conditions[cond].words_in_model for cond in self.condition_names[0]]]
            words_cond1 = [w for s in words_cond1 for w in s]
            nwords1 = len(words_cond1)
            words_cond2 = [w for w in [experi.conditions[cond].words_in_model for cond in self.condition_names[1]]]
            words_cond2 = [w for s in words_cond2 for w in s]
            all_words = words_cond1+words_cond2
            self.permuted_vectors = np.zeros([experi.nperm, experi.model.ndim])
            for i in range(experi.nperm):
                pw = np.random.permutation(all_words)
                tmpcond1 = Condition(pw[:nwords1],experi.model)
                tmpcond2 = Condition(pw[nwords1:],experi.model)
                self.permuted_vectors[i,:] = self.make_contrast_vector([tmpcond1],[tmpcond2])
        print('generated {0} randomized vectors for contrast {1}'.format(experi.nperm,self.condition_names))

    # A contrast sometimes comprises a collection of conditions (e.g. check Davis2004).
    # We take the mean over the condition feature vectors for each contrast
    # FIXME: we can use nWords to normalize according to how many words we have in each sub condition
    def make_contrast_vector(self, cond_1, cond_2):
        vector1 = np.vstack([cond.vector for cond in cond_1]).mean(0)
        vector2 = np.vstack([cond.vector for cond in cond_2]).mean(0)
        return vector1 - vector2

    def run(self, subject_group, do_pmap = False):
        return subject_group.run(self, do_pmap = do_pmap)

class Coordinates:

    def __init__(self, xyz, name=None, zscore=None, size=8, **extra_info):
        self.xyz = xyz
        self.name = name
        self.zscore = zscore
        self.size = size
        self.extra_info = extra_info

    def get_mni_roi_mask(self):

        print("in get_mni_roi_mask !")

        """Given an MNI coordinate xyz (in mm) returns the ROI mask in MNI space."""
        radius = self.size

        # Load MNI template image
        default_template = os.path.join(FSLDIR, "data", "standard", "MNI152_T1_1mm_brain.nii.gz")
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

# print(Experiment())