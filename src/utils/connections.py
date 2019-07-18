from serializer.renders.json import JSONRender
import requests
from hubs.config import Config
import json

def update_contrast_result(message):
    # res_dict = {'contrast_results':  message }
    # print("res_dict = ", res_dict)
    r = requests.post(Config.update_contrast_url, data = message )