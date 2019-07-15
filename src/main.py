from hubs.subjects import Subjects
from hubs.config import Config
from hubs.logger import Logger

import time

from hubs.semanticmodels import SemanticModels

from models.experiment import Experiment

inputs = {u'contrasts': {u'contrast1': {u'do_perm': True, u'num_perm': 1000, u'condition1': [u'cond1'], u'figures': [], u'condition2': [u'cond2'], u'coordinates': []}}, u'stimuli': {u'cond1': {u'type': u'word_list', u'value': u'one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, hundred, thousand, million, half, quarter, pair, few, several, many, some, less, more'}, u'cond2': {u'type': u'word_list', u'value': u'house, building, hotel, office, parking, lot, park, street, road, sidewalk, highway, path, field, mountain, forest, beach, cinema, restaurant, bistro, shop, store'}}, u'DOI': u'', u'coordinate_space': u'mni', u'do_perm': False}


class Main:

    def start(self):
        # Logger.debug("trying to start")
        # print(Config.semanticmodels)
        # print(SemanticModels.english1000)
        # begin = time.time()
        # print(Subjects.english1000)
        # print(time.time()-begin)

        Experiment()(inputs)


if __name__ == "__main__":
    Main().start()
