import requests
import json
import numpy as numpy
from pprint import pprint


def getTextFromMidi(fileName):
    file_ = {'file': (fileName, open(fileName, 'rb'))}
    r = requests.post("http://my-own-it.de/toText", files=file_)
    print(r.status_code, r.reason)
    return r.text

def getMidiFromText(dataAsText,name):
    r = requests.post("http://my-own-it.de/toMid", data={"midAsJson": dataAsText, "name": name})
    print(r.status_code, r.reason)
    return r.text

def createTextFileFromMidiData(data):

    for data in data["tracks"]:
        noteVector = numpy.zeros(88)
        trackArray = []
        deltaTime = 0
        for time in data:
            if("deltaTime" in time):
                deltaTime += time["deltaTime"]
            if("noteNumber" in time):
                if(time["noteNumber"] < 89):
                    if(time["subtype"] == 'noteOn'):
                        noteVector[time["noteNumber"]-1] = 1
                    if (time["subtype"] == 'noteOff'):
                        noteVector[time["noteNumber"]-1] = 0
                    trackArray.append(noteVector)
                    print(noteVector)
                #print(time)
            #print(deltaTime)
        #print(trackArray)

dataAsText = getTextFromMidi("fp-1all.mid")
dataAsObject = json.loads(dataAsText)
createTextFileFromMidiData(dataAsObject)
#pprint(dataAsObject)
result = getMidiFromText(dataAsText,"fp1")
print(result)

