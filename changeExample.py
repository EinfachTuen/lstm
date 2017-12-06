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

import KTimage as kt


def loadMidiFromText():
    with open ('midiBach.txt', 'r') as myfile:
        data = myfile.readlines()
        return data

def createInputArray():
    linesArray = []
    for line in loadMidiFromText():
        splittedLine = line.split("n=")
        try:
            secondPart = splittedLine[1].split(" v=")
            note = secondPart[0]
            velocity = secondPart[1].split("\n")[0]
            #print(velocity)
            #print(note)
            keyboard = numpy.zeros(88)
            if velocity == "100":
                note = int(note)
                keyboard[note-1] = 1
                #print("an"+str(keyboard))
            if velocity == "0":
                note = int(note)
                keyboard[note-1] = 0
                #print("aus"+str(keyboard))

            linesArray.append(keyboard)
            #print(secondPart)
        except IndexError:
            print("Couldn't find informations"+str(splittedLine))
    return linesArray
inputArray = numpy.asarray(createInputArray())

data = inputArray[:-1] # all but last
target = inputArray[1:] # all but first

print("inputArray",inputArray.shape)

data = data.reshape((2037, 1, 88))
# target = numpy.array([[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1]])
data = target.reshape((2037, 1, 88))

print("target shape " +str(target.shape))
print(target)
print(data.shape)
model = Sequential()
model.add(LSTM(88, input_shape=(1,88)))
model.add(Dense(88, activation='softmax'))
optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

x_train = numpy.asarray(data)
y_train = numpy.asarray(target)


model.fit(x_train, y_train, batch_size=88, epochs=5)
score = model.evaluate(x_train, y_train, batch_size=88)
result = model.predict(x_train, batch_size=88)
#print(score)
#print(result)
endresult = result
i = 0

for element in result:
    j = 0
    for prob in element:
        resultBin = 0
        if(prob > 0.5):
            print(prob)
            resultBin = 1
        endresult[i][j] = resultBin
        print(str(prob))
        print(str(resultBin))
        j = j + 1
    i = i + 1




numpy.savetxt("result.txt",result,fmt='%i')


