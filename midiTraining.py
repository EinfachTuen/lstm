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

import midiStringParts


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


def convertToMidi(x):
    result = numpy.asarray(x)
    timeStep = 120
    print(len(result))
    NotePartMidiString = ""
    lastNoteActive = 0
    for resultLine in range(0, len(result)):
        noteActive = False   
        for resultNotePosition in range(0, result[resultLine].size-1):
            if result[resultLine][resultNotePosition] == 1:
                noteActive = True
                lastNoteActive = resultNotePosition        
        if noteActive: 
            NotePartMidiString += "\n"+str(timeStep)+" On ch=1 n="+str(lastNoteActive)+" v=100"
            timeStep += 120
        else: 
            NotePartMidiString += "\n"+str(timeStep)+" On ch=1 n="+str(lastNoteActive)+" v=0"
    return midiStringParts.midiStartString()+""+NotePartMidiString+"\n"+midiStringParts.midiEndeString()
   
    

    
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
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

x_train = numpy.asarray(data)
y_train = numpy.asarray(target)


model.fit(x_train, y_train, batch_size=88, epochs=5)
score = model.evaluate(x_train, y_train, batch_size=88)
result = model.predict(x_train[:-10], batch_size=88)

endresult = result

i= 0
for element in result:
    j = 0
    for prob in element:
        resultBin = 0
        if(prob > 0.5):
            print(prob)
            resultBin = 1
        endresult[i][j] = resultBin
        #print(str(prob))
        #print(str(resultBin))
        j = j + 1
    i = i + 1

finalString = convertToMidi(result)
print(finalString)
text_file = open("result55.txt", "w")
text_file.write(finalString)
text_file.close()
#numpy.savetxt("result55.txt",diggaString)


