import os
import time
import cortex
import numpy as np
from subject import Subject
from subject_group import SubjectGroup
from utils import load_config, read_json
from subject_analyses import SubjectAnalysis
from experiment import Experiment, ModelHolder

class Replicate():

    def __init__(self):
        
        self.json_dir = 'jsons'

        config = load_config(self.json_dir)
        build_dir = config['build_dir']
        model_dir = config['model_dir']
        self.model_holder = ModelHolder(self.json_dir)
        tmp_image_dir = './static/simulate/'
        static_dir = 'static'

        if not os.path.exists(build_dir):
            os.mkdir(build_dir)
        
        if not os.path.exists(os.path.join(build_dir, static_dir)):
            os.mkdir(os.path.join(build_dir, static_dir))

        sub_analyses = [WebGL(tmp_image_dir = tmp_image_dir, dopmap = False)]
        sub_analyses_with_p = [WebGL(tmp_image_dir = tmp_image_dir, dopmap = True)]

        subjects_info = read_json('subjects.json', self.json_dir)
        print('[Subject_info] '+ str(subjects_info))
        subjects = []

        for key in sorted(subjects_info.keys()):
            s = Subject(name = key,
                        model_type = 'english1000',
                        model_dir = model_dir,
                        analyses = [sub_analyses, sub_analyses_with_p],
                        **subjects_info[key]
                        )
            subjects.append(s)

        from group_analyses import Mean, Mean_two
        grp_analyses = [Mean([WebGLGroup(tmp_image_dir = tmp_image_dir, dopmap = False)])]

        webglgrp = WebGLGroup(tmp_image_dir = tmp_image_dir, dopmap = True)
        savepmaps = SavePmaps(tmp_image_dir = tmp_image_dir)
        grp_analyses_with_p = [Mean_two([webglgrp, savepmaps], smooth = None, pmap = True)]

        self.subject_group = SubjectGroup(subjects, [grp_analyses, grp_analyses_with_p])
        self.nan_mask = np.load('MNI_nan_mask.npy')
        self.tmp_image_dir = tmp_image_dir

        print("Create a new structure!")


    def run(self, info):
        experi = Experiment(model_holder = self.model_holder, name = 'temp', image_dir = '.', model_type = 'english1000', json_dir=self.json_dir, **info)
        res = experi.run(self.subject_group, do_pmap=info['do_perm'])
        result = {}
        result['group'] = res[0][0][0][0]
        for i in range(len(self.subject_group.subjects)):
            result['s_{}'.format(i+1)] = res[0][1+i][0]

        if info['do_perm']:
            result['pmaps'] = res[0][0][1][0]
        else:
            result['pmaps'] = ''
        return result


class WebGL(SubjectAnalysis):

    def __init__(self, dopmap = True, tmp_image_dir = './tmp_image'):
        self.dopmap = dopmap
        self.open_browser = False
        self.tmp_image_dir = tmp_image_dir

    def __call__(self, contrast_data):
        # Save static viewer
        contrast_data.vmax = 3
        contrast_data.vmin = -3
        
        contrast_data.data[contrast_data.ref_to_subject.voxels_predicted == 0] = np.nan
        res_dict = {'contrast': contrast_data}

        if self.dopmap:
            res_dict['pmap'] = contrast_data.thresholded_contrast_05
            res_dict['pmap'].data[contrast_data.ref_to_subject.voxels_predicted==0]=np.nan
            res_dict['pmap'].cmap = 'Blues'
            res_dict['pmap'].vmin = 0
            res_dict['pmap'].vmax = 1.25

        jsonstr = cortex.webgl.make_static_light(self.tmp_image_dir,res_dict)
        return jsonstr

class WebGLGroup(SubjectAnalysis):

    def __init__(self, dopmap = True, tmp_image_dir = '~/tmp_images'):
        self.dopmap = dopmap
        self.open_browser = False
        self.tmp_image_dir = tmp_image_dir

    def __call__(self, contrast):
        
        if not self.dopmap:
            contrast.vmax = 2
            contrast.vmin = -2
            contrast.data[contrast.data == 0] = np.nan
            res_dict = {'contrast': contrast}
        else:
            contrast_not_pmap = contrast[0]
            contrast_pmap = contrast[1]
            contrast_not_pmap.vmax = 2
            contrast_not_pmap.vmin = -2
            contrast_not_pmap.data[contrast_not_pmap.data == 0] = np.nan
            res_dict = {'contrast': contrast_not_pmap, 'pmap': contrast_pmap}

        jsonstr = cortex.webgl.make_static_light(self.tmp_image_dir,res_dict)
        return jsonstr


class SavePmaps(SubjectAnalysis):

    def __init__(self, tmp_image_dir = '~/tmp_images'):
        self.tmp_image_dir = tmp_image_dir

    def __call__(self, contrast):

        sub_volume_pmap = contrast[3]
        tmp = [s.data for s in sub_volume_pmap]
        stacked_tmp = np.stack(tmp)
        stacked_tmp[np.isnan(stacked_tmp)] = 0
        stacked_tmp = stacked_tmp.astype(bool)

        filename = tempfile.mktemp(suffix='.h5f', dir=self.tmp_image_dir, prefix='pmaps-')
        with h5py.File(filename, 'w') as hf:
            hf.create_dataset("pmaps", data=stacked_tmp)

        return filename

r = Replicate()
# info = {u'contrasts': {u'contrast1': {u'condition1': [u'cond1'], u'figures': [], u'condition2': [u'cond2'], u'coordinates': []}}, u'stimuli': {u'cond1': {u'type': u'word_list', u'value': u'one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, hundred, thousand, million, half, quarter, pair, few, several, many, some, less, more'}, u'cond2': {u'type': u'word_list', u'value': u'house, building, hotel, office, parking, lot, park, street, road, sidewalk, highway, path, field, mountain, forest, beach, cinema, restaurant, bistro, shop, store'}}, u'DOI': u'', u'coordinate_space': u'mni', u'do_perm': False}
info = {"stimuli": {"number": {"type": "word_list", "value": "one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, hundred, thousand, million, half, quarter, pair, few, several, many, some, less, more"}, "quantity": {"type": "word_list", "value": "one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, hundred, thousand, million, half, quarter, pair, few, several, many, some, less, more"}}, "contrasts": {"contrast1": {"figures": [], "coordinates": [], "condition1": ["number"], "condition2": ["quantity"]}}, "do_perm": False, "coordinate_space": "mni", "DOI": ''}

r.run(info)