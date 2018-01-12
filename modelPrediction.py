import numpy as numpy

from keras.models import load_model

import json
import midiConverter

model = load_model('my_model.h5')

actualTrain = numpy.loadtxt("xTrain.txt")
result = numpy.empty([1, 88])
for x in range(0,2000):
    if x > 0:
        actualTrain = actualTrain[1:actualTrain.shape[0]]
        partResult = (model.predict(numpy.array([actualTrain]), batch_size=32))
        actualTrain = numpy.append(actualTrain,partResult,axis=0)
        result = numpy.append(result,partResult,axis=0)
    else:
        partResult = (model.predict(numpy.array([actualTrain]), batch_size=32))
        print("partResult" + str(partResult.shape))
        actualTrain = numpy.append(actualTrain,partResult,axis=0)
        print("actualTrain" + str(actualTrain.shape))
        result[0] = partResult[0]

i = 0
for element in result:
    j = 0
    for prob in element:
        resultBin = 0
        if (prob > 0.5):
            resultBin = 1
            result[i][j] = resultBin
        j = j + 1
    i = i + 1

numpy.savetxt("output2.txt",result,fmt='%i')

finalString = midiConverter.convertToMidiTrack(result)
print(finalString)
text_file = open("result55.txt", "w")
text_file.write(json.dumps(finalString, indent=2))
text_file.close()
uploadResult = midiConverter.getMidiFromText(finalString,"testPy")
print(uploadResult+".mid")



