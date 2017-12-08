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
inputArray = createInputArray()

print("inputArray",len(inputArray))
newInputArray = numpy.zeros((11,200,88))
print(numpy.asarray(inputArray[0]).shape)

for j in range(11):
    for i in range(200):
        newInputArray[j][i] = inputArray[i*j]

print(newInputArray.shape)
model = Sequential()
model.add(LSTM(128, input_shape=(11,1,88)))
model.add(Dense(88))
model.add(Activation('softmax'))
optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

x_train = numpy.asarray(inputArray[:-1])
y_train = numpy.asarray(inputArray[1:])
print(numpy.argwhere(x_train))
print(numpy.argwhere(y_train))

model.fit(x_train, y_train, batch_size=280, epochs=1)
score = model.evaluate(x_train, y_train, batch_size=16)
result = model.predict(x_train[0], batch_size=16)
print(score)
print(result)
numpy.savetxt("result.txt",result)

def printKT(Q):
    kt.exporttiles(array=Q, height=2037, width=88, filename="results/obs_M_1.pgm")
print(numpy.argwhere(result))
printKT(result.reshape(88*2037))