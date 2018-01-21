import numpy as numpy
import requestTests

from keras.models import load_model

import json
import midiConverter

model = load_model('./models/noteModel.h5')
model_duration = load_model('./models/durationsModel.h5')

actualTrain = numpy.loadtxt("./log/x2Train.txt")
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
    for prob in element:
        resultBin = 0
        if (prob > 0.5):
            resultBin = 1
            if(j < 128):
                result[i][j] = resultBin
        j = j + 1
    i = i + 1

numpy.savetxt("./log/output2.txt",result,fmt='%.3f')

requestTests.covertArrayToJSON(result.tolist())




