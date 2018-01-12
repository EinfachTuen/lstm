import requests
import json
import numpy as numpy
from pprint import pprint


def getTextFromMidi(fileName):
    file_ = {'file': (fileName, open(fileName, 'rb'))}
    r = requests.post("http://localhost/toText", files=file_)
    print(r.status_code, r.reason)
    return r.text

def getMidiFromText(dataAsText,name):
    r = requests.post("http://localhost/toMidNewConvert", {"midAsJson": json.dumps(dataAsText), "name": name})
    print(r.status_code, r.reason)
    return r.text

def createTextFileFromMidiData(data):
    text_file = open("data.txt", "w")
    text_file.write(json.dumps(data, indent=2))
    text_file.close()
    trackNo = 0
    print(data)
    for data in data["tracks"]:
        trackArray = []
        deltaTime = 0
        for event in data:
            if("noteNumber" in event):
                if(event["noteNumber"] < 89):
                    if(event["subtype"] == 'noteOn'):
                        noteVector = numpy.zeros(88)
                        noteVector[event["noteNumber"]-1] = 1
                        trackArray.append(numpy.copy(noteVector))
        if(len(trackArray) > 0):
            result = trackArray
            #print(trackArray)
    return numpy.asarray(result)

def getMidiFromFile():
    dataAsText = getTextFromMidi("fp-1all.mid")
    dataAsObject = json.loads(dataAsText)
    result = createTextFileFromMidiData(dataAsObject)
    print("shape: "+str(result.shape))
    return result

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


#getMidiFromFile()


