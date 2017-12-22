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
    smallestDelta = 9999
    trackNo = 0
    for data in data["tracks"]:
        noteVector = numpy.zeros(88)
        trackArray = []
        deltaTime = 0
        for time in data:
            if("noteNumber" in time):
                if ("deltaTime" in time):
                    deltaTime += time["deltaTime"]
                    if (time["deltaTime"] < smallestDelta and time["deltaTime"] > 0):
                        smallestDelta = time["deltaTime"]

                if(time["noteNumber"] < 89):
                    if(time["subtype"] == 'noteOn'):
                        noteVector[time["noteNumber"]-1] = 1
                    if (time["subtype"] == 'noteOff'):
                        noteVector[time["noteNumber"]-1] = 0
                    if ("deltaTime" in time):
                        trackArray.append(numpy.copy(noteVector))
        if(len(trackArray) > 0):
            result = trackArray
            #print(trackArray)
    return numpy.asarray(result)

def convertToMidiTrack(ingoing):
    lastNoteActive = 0
    result = []
    for resultLine in range(0, len(ingoing)):
        resultObject = {"deltaTime": 666,
         "channel": 0,
         "type": 'channel',
         "noteNumber": 99,
         "velocity": 0,
         "subtype": 'noteOff'}
        noteActive = False

        for resultNotePosition in range(0, ingoing[resultLine].size-1):
            if ingoing[resultLine][resultNotePosition] == 1:
                noteActive = True
                lastNoteActive = resultNotePosition
        if noteActive:
            resultObject["deltaTime"] = 120
            resultObject["subtype"] = "noteOn"
            resultObject["noteNumber"] = lastNoteActive
        else:
            resultObject["deltaTime"] = 0
            resultObject["subtype"] = "noteOff"
            resultObject["noteNumber"] = lastNoteActive
        result.append(resultObject)
    return result

def getMidiFromFile():
    dataAsText = getTextFromMidi("fp-1all.mid")
    dataAsObject = json.loads(dataAsText)
    result = createTextFileFromMidiData(dataAsObject)
    print("shape: "+str(result.shape))
    return result
    # pprint(dataAsObject)
    # result = getMidiFromText(dataAsText, "fp1")
    # print(result)

#getMidiFromFile()


