import numpy as numpy
import requestTests
import os

from keras.models import load_model
import random
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def makePrediction(model,model_duration,actualTrain,midiName,channel):
    print(str(actualTrain.ndim))
    if(actualTrain.ndim == 1):
        actualTrain = numpy.array([actualTrain])
    print(str(actualTrain.ndim))
    result = numpy.empty([1, 129])
    for x in range(0,500):
        if x > 0:
            actualTrain = actualTrain[1:actualTrain.shape[0]]
            partResult = (model.predict(numpy.array([actualTrain]), batch_size=32))
            duration = model_duration.predict(numpy.array([actualTrain]), batch_size=32)
            newresult = numpy.append(partResult[0], duration)
            partResult = newresult
            actualTrain = numpy.append(actualTrain, [partResult],axis=0)
            result = numpy.append(result,[partResult],axis=0)
        else:
            partResult = (model.predict(numpy.array([actualTrain]), batch_size=32))
            duration = model_duration.predict(numpy.array([actualTrain]), batch_size=32)
            newresult= numpy.append(partResult[0], duration)
            partResult=newresult
            actualTrain =  numpy.append(actualTrain,[partResult],axis=0)
            result[0] = partResult[0]

    print("finsied saves now")
    i = 0
    for element in result:
        j = 0
        maxProb = 0
        maxElement = -1
        for prob in element:
            resultBin = 0
            if (prob > maxProb and j < 128):
                    #print(str(prob))
                    maxElement = j
                    maxProb = prob
            if (j < 128):
                result[i][j] = resultBin
            j = j + 1

        if(maxElement > 0):
            result[i][maxElement] = 1
        i = i + 1
    numpy.savetxt("./log/output2.txt",result,fmt='%.3f')

    return requestTests.covertArrayToJSON(result.tolist(),midiName,channel)


def makeSpecialPrediction(model,model_duration,actualTrain):
    print(str(actualTrain.ndim))
    if(actualTrain.ndim == 1):
        actualTrain = numpy.array([actualTrain])
    print(str(actualTrain.ndim))
    result = numpy.empty([1, 129])
    for x in range(0,500):
        if x > 0:
            actualTrain = actualTrain[1:actualTrain.shape[0]]
            partResult = (model.predict(numpy.array([actualTrain]), batch_size=32))

            #duration = model_duration.predict(numpy.array([actualTrain]), batch_size=32)
            newresult = numpy.append(partResult[0], partResult[1])
            partResult = newresult
            #print("partResult" + str(partResult.shape))
            actualTrain = numpy.append(actualTrain, [partResult],axis=0)
            result = numpy.append(result,[partResult],axis=0)
        else:
            partResult = (model.predict(numpy.array([actualTrain]), batch_size=32))
            # duration = model_duration.predict(numpy.array([actualTrain]), batch_size=32)
            newresult = numpy.append(partResult[0], partResult[1])
            partResult = newresult
            #print("partResult" + str(partResult.shape))
            actualTrain =  numpy.append(actualTrain,[partResult],axis=0)
            #print("actualTrain" + str(actualTrain.shape))
            result[0] = partResult[0]

    print("finsied saves now")
    i = 0
    for element in result:
        j = 0
        maxProb = 0
        maxElement = -1
        for prob in element:
            resultBin = 0
            if (prob > maxProb and j < 128):
                    print(str(prob))
                    maxElement = j
                    maxProb = prob
            if (j < 128):
                result[i][j] = resultBin
            j = j + 1

        if(maxElement > 0):
            result[i][maxElement] = 1
        i = i + 1
    numpy.savetxt("./log/output2.txt",result,fmt='%.3f')

    return requestTests.covertArrayToJSON(result.tolist())

def getFolderContent():
    newArray = os.listdir("./models/")
    newDictionary ={}
    for folder in newArray:
        newDictionary[""+folder] =  os.listdir("./models/"+str(folder))
    return newDictionary

#http://127.0.0.1:5000/getPrediction?folder=bachOneChannel&channel=73
@app.route('/getPrediction')
def getPrediction():
    midiName = "test1"
    folder = request.args.get('folder')
    channel = request.args.get('channel')
    model = load_model('./models/' +str(folder)+'/'+ str(channel) + '_noteModel.h5')
    model_duration = load_model('./models/' +str(folder)+'/'+ str(channel) + '_durationModel.h5')
    print("got request")
    starttrain = numpy.loadtxt('./models/' +str(folder)+'/'+  str(channel) + "_x2Train.txt")
    print("trainShape" + str(starttrain.shape))
    midiFileName = makePrediction(model,model_duration,starttrain,midiName,channel)
    return "<a href='http://localhost/"+midiFileName+".mid' >"+midiFileName+"</a>"
#127.0.0.1:5000/getModels
@app.route('/getModels')
def getModels():
    print("got getModels request")
    return jsonify(getFolderContent())

def runPrediction(folderName,channel,midiName):
    noteModelPath = './models/' + folderName+ '/' + str(channel) + '_noteModel.h5'
    durationModelPath = './models/' + folderName + '/' + str(channel) + '_durationModel.h5'
    model = load_model(noteModelPath)
    model_duration = load_model(durationModelPath)
    print("got request")
    startTrain = numpy.loadtxt('./models/' + folderName + '/' + str(channel) + "_x2Train.txt")
    print("trainShape" + str(startTrain.shape))
    i = 0
    for notes in startTrain:
        newNotes = numpy.zeros(129)
        randomActiveNote = random.randint(70, 90)
        newNotes[randomActiveNote] = 1
        startTrain[i] = newNotes
    numpy.savetxt('./models/' + folderName + '/' + str(channel) + "_randomInput.txt", startTrain, fmt='%.3f')

    midiFileName = makePrediction(model, model_duration, startTrain,midiName,channel)
    return midiFileName

if __name__ == '__main__':
    app.run()
