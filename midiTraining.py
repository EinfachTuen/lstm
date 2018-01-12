# -*- coding: utf-8 -*-
import numpy as numpy

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.utils import to_categorical
from keras.optimizers import RMSprop
from keras.layers import Activation

import json
import midiStringParts
import midiConverter

def loadMidiFromText():
    with open ('midiBach.txt', 'r') as myfile:
        data = myfile.readlines()
        return data
    
inputArray = midiConverter.getMidiFromFile()

data = inputArray[:-1] # all but last
target = inputArray[1:] # all but first


# target = numpy.array([[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1]])
data = target.reshape((1779, 1, 88))
#
# text_file = open("target Data.txt", "w")
# text_file.write(json.dumps(target[0], indent=2))
# text_file.close()

print("target shape " +str(target.shape))
print(target)
print(data.shape)
model = Sequential()
model.add(LSTM(512, input_shape=(1,88)))
model.add(Dense(88, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

x_train = numpy.asarray(data)
y_train = numpy.asarray(target)
train_size = 10
testTrain = numpy.zeros((train_size, 1, 88))
# for i in range(0, train_size):
#     x = numpy.random.random_integers(0, 87)
#     testTrain[i][0][x] = 1

outputTest = testTrain.tolist()
text_file = open("resultTrain.txt", "w")
text_file.write(json.dumps(outputTest, indent=2))
text_file.close()

print("X_TRAIN" + str(x_train))

model.fit(x_train, y_train, batch_size=1, epochs=1)
score = model.evaluate(x_train, y_train, batch_size=1)
result = model.predict(testTrain, batch_size=1)
numpy.savetxt('resultAfterSoftmaxPredict.txt',result)

endresult = result

i = 0
for element in result:
    j = 0
    for prob in element:
        resultBin = 0
        if (prob > 0.5):
            # print(prob)
            resultBin = 1
        endresult[i][j] = resultBin
        # print(str(prob))
        # print(str(resultBin))
        j = j + 1
    i = i + 1

numpy.savetxt('resultTTT.txt',endresult,  fmt='%i')

print("inputArray",inputArray.shape)
print("target",target.shape)
print("data",data.shape)

finalString = midiConverter.convertToMidiTrack(endresult)
print(finalString)
text_file = open("result55.txt", "w")
text_file.write(json.dumps(finalString, indent=2))
text_file.close()



