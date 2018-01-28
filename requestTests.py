import requests
import json

def GetNotesPlusFloatDuration():
    r = requests.post("http://localhost/CombinedDurationAsFloat")
    input = json.loads(r.text)
    return input


def covertArrayToJSON(resultVektorArray):
    r = requests.post("http://localhost/convertArrayToJSON", {"midAsJson": json.dumps(resultVektorArray), "name": "Bach50E.50SL.3000BS.256.155"})
    return r.text

