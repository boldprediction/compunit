from hubs.subjects import Subjects
from hubs.config import Config
from hubs.logger import Logger
from hubs.semanticmodels import SemanticModels
from models.experiment import Experiment
import time, json, unittest

class TestApp(unittest.TestCase):

   def setUp(self):
       self.input = {u'contrasts': {u'contrast1': {u'condition1': [u'cond1'], u'figures': [], u'condition2': [u'cond2'], u'coordinates': []}}, u'stimuli': {u'cond1': {u'type': u'word_list', u'value': u'one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, hundred, thousand, million, half, quarter, pair, few, several, many, some, less, more'}, u'cond2': {u'type': u'word_list', u'value': u'house, building, hotel, office, parking, lot, park, street, road, sidewalk, highway, path, field, mountain, forest, beach, cinema, restaurant, bistro, shop, store'}}, u'DOI': u'', u'coordinate_space': u'mni', u'do_perm': False}

   def test_experiment_e2e(self):

       result = Experiment()(self.input)
       #self.assertEqual(result, "image") Add assert here


def suite():

   suite = unittest.TestSuite()
   suite.addTests(
       unittest.TestLoader().loadTestsFromTestCase(TestApp)
   )
   return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
