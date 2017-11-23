# -*- coding: utf-8 -*-
import numpy as numpy

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM



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
print(inputArray)

model = Sequential()

model.add(Embedding(88, output_dim=88))
model.add(LSTM(128))
model.add(Dropout(0.5))
model.add(Dense(88, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

x_train = numpy.asarray(inputArray[:-1])
y_train = numpy.asarray(inputArray[1:])

model.fit(x_train, y_train, batch_size=1032, epochs=10)
score = model.evaluate(x_train, y_train, batch_size=1032)
result = model.predict(x_train, batch_size=1032)
print(score)
print(result.shape)
    