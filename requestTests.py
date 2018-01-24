import requests
import json
import numpy as numpy
from pprint import pprint


def getMidiAsArray():
    r = requests.post("http://localhost/withDurationToMidi")
    newArray = numpy.asarray(json.loads(r.text))
    print(newArray[0])
    numpy.savetxt("./log/newTest.txt",newArray[0],fmt='%i')
    return numpy.asarray(newArray[0])

def GetNotesPlusFloatDuration():
    r = requests.post("http://localhost/CombinedDurationAsFloat")
    input = json.loads(r.text)
    print(input)
    return input

def covertArrayToJSON(resultVektorArray):
    r = requests.post("http://localhost/convertArrayToJSON", {"midAsJson": json.dumps(resultVektorArray), "name": "tryOne2"})
    print(r.status_code, r.reason,r.text)
    return r.text

