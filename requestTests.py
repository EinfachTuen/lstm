import requests
import json
import numpy as numpy
from pprint import pprint

def GetNotesPlusFloatDuration():
    r = requests.post("http://localhost/CombinedDurationAsFloat")
    input = json.loads(r.text)
    return input

def covertArrayToJSON(resultVektorArray,midiName):
    r = requests.post("http://localhost/convertArrayToJSON", {"midAsJson": json.dumps(resultVektorArray), "name": midiName})
    return r.text

