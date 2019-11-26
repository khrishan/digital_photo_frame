import json
import os

def getConfig(location):
    with open(location) as config_file:
        return json.load(config_file)