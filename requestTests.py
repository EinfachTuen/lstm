import requests
import json
import numpy as numpy
from pprint import pprint


def getMidiAsArray():
    r = requests.post("http://localhost/withDurationToMidi")
    newArray = numpy.asarray(json.loads(r.text))
    print(newArray[0])
    numpy.savetxt("newTest.txt",newArray[0],fmt='%i')
    return numpy.asarray(newArray[0])

# midi =numpy.asarray(getMidiAsArray())
# print(str(midi.shape))