import os
import time
import requests,json


class Replicate():
    #URI = 'http://ec2-54-198-142-139.compute-1.amazonaws.com:3000/api/trips/update/bot/arrival'
    httpUrl = "http://16237457.ngrok.io/api/update_contrast"
        
    def run(self, info):
        print("#############      inovked run      ###########")
        #res = {	"station": "MAINTENANCE_START"}
        res = {"contrast_id": "Jxbojag","MNIstr": "test","subjstr": "test"}
        res = json.dumps(res)
        print(requests.post(self.httpUrl, data = res))

r = Replicate()
info = {u'contrasts': {u'contrast1': {u'condition1': [u'cond1'], u'figures': [], u'condition2': [u'cond2'], u'coordinates': []}}, u'stimuli': {u'cond1': {u'type': u'word_list', u'value': u'one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, hundred, thousand, million, half, quarter, pair, few, several, many, some, less, more'}, u'cond2': {u'type': u'word_list', u'value': u'house, building, hotel, office, parking, lot, park, street, road, sidewalk, highway, path, field, mountain, forest, beach, cinema, restaurant, bistro, shop, store'}}, u'DOI': u'', u'coordinate_space': u'mni', u'do_perm': False}
r.run(info)