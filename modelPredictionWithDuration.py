import numpy as numpy
import requestTests

from keras.models import load_model

import json
import midiConverter
from flask import Flask
from flask import jsonify

app = Flask(__name__)

channelNumber = 30

model = load_model('./models/' + str(channelNumber) + '_noteModel.h5')
model_duration = load_model('./models/' + str(channelNumber) + '_durationsModel.h5')

def makePrediction():
    actualTrain = numpy.loadtxt("./log/"+str(channelNumber)+"_x2Train.txt")
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
            #print("partResult" + str(partResult.shape))
            actualTrain = numpy.append(actualTrain, [partResult],axis=0)
            result = numpy.append(result,[partResult],axis=0)
        else:
            partResult = (model.predict(numpy.array([actualTrain]), batch_size=32))
            #print(partResult)
            duration = model_duration.predict(numpy.array([actualTrain]), batch_size=32)
            newresult= numpy.append(partResult[0], duration)
            partResult=newresult
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


@app.route('/getPrediction')
def getPrediction():
    print("got request")
    return "<a href='http://localhost/"+makePrediction()+".mid' >"+makePrediction()+"</a>"

if __name__ == '__main__':
    app.run()
