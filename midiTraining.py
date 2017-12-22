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
    




def shapeData(sequence_length):    
    input_data = []
    output_data = []
    
    for i in range(0, (inputArray.shape[0] - sequence_length), 1):
        input_sequence = inputArray[i:i+sequence_length]
        output_sequence = inputArray[i+sequence_length]    
        input_data.append(input_sequence)
        output_data.append(output_sequence)
    
    input_data = numpy.asarray(input_data)
    output_data = numpy.asarray(output_data)
    
    return (input_data, output_data)

inputArray = midiConverter.getMidiFromFile()
sequence_length = 10

print("ARRAY"+str(inputArray.shape))
data,target = shapeData(sequence_length)
print("DATA"+str(data.shape))
print("TARGET"+str(target.shape))

#data = inputArray[:-1] # all but last
#target = inputArray[1:] # all but first

print("inputArray",inputArray.shape)

#data = data.reshape((1779, 1, 88))
# target = numpy.array([[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
#    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1]])
#data = target.reshape((1779, 1, 88))

print("target shape " +str(target.shape))
print(target)
print(data.shape)
model = Sequential()
model.add(LSTM(88, input_shape=(10,88)))
model.add(Dense(88, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

x_train = data
y_train = numpy.asarray(target)
print("x_train"+str(x_train.shape))
print("y_train"+str(y_train.shape))

#testTrain = numpy.zeros((2037, 1, 88))
#for i in range(0, 2036):
#    x = numpy.random.random_integers(0, 87)
#    testTrain[i][0][x] = 1
#
#print("X_TRAIN" + str(x_train))

model.fit(x_train, y_train, batch_size=32, epochs=100)
score = model.evaluate(x_train, y_train, batch_size=32)
result = model.predict(x_train, batch_size=32)

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

finalString = midiConverter.convertToMidiTrack(result)
print(finalString)
text_file = open("result55.txt", "w")
text_file.write(json.dumps(finalString, indent=2))
text_file.close()



