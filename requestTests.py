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


def GetMidiJSONWithDurationHotEncoded():
    r = requests.post("http://localhost/DurationHotEncoded")
    input = json.loads(r.text)
    GetInputElements(input)



# def PrepareVektors(MidiWithDurations):
#     numpy.zeros
#     notesWithDurations = MidiWithDurations["track"]
#     print(notesWithDurations)
#

def GetNotesPlusFloatDuration():
    r = requests.post("http://localhost/DurationAsFloat")
    input = numpy.asarray(json.loads(r.text),dtype=numpy.float32)
    numpy.savetxt("newTest.txt",input,fmt='%.3f')
    print(input.dtype)
    print(input)
    return input

GetNotesPlusFloatDuration()