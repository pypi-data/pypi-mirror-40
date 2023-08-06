import os
import json

path = os.path.dirname(os.path.abspath(__file__)) + '/data/jp_geocode.json'

with open(path) as f:
    df = json.load(f)

def jpgeocode(name):
    return df[name]

