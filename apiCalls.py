import requests
import json


'''
gets Notes as oneHotEncoded plus duration and time as float32
'''
def GetNotesPlusFloatDuration():
    r = requests.post("http://localhost/getJSOnOfMidiFolder")
    input = json.loads(r.text)
    return input

'''
Convert Output Array to Midi File, the Midifile will be stowed on the server.
'''
def covertArrayToJSON(resultVektorArray,midiName,channel):
    r = requests.post("http://localhost/convertArrayToMidi", {"midAsJson": json.dumps(resultVektorArray), "name": midiName, "channel":channel})
    return r.text

#To grap one big JSON with channels inside for newest not correct working model
'''
def GetAllTogether():
    r = requests.post("http://localhost/withAnyThingToInputArray")
    input = json.loads(r.text)
    return input
'''

