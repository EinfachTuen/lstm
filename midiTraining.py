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



inputArray = midiConverter.getMidiFromFile()
sequence_length = 10
#print all
startAsString = midiConverter.convertToMidiTrack(inputArray)
numpy.savetxt("inputArray.txt",inputArray,fmt='%i')
uploadResult = midiConverter.getMidiFromText(startAsString,"inputArray")

print("ARRAY"+str(inputArray.shape))

def shapeData(sequence_length):
    input_data = []
    output_data = []

    for i in range(0, (inputArray.shape[0] - sequence_length), 1):
        input_sequence = inputArray[i:i + sequence_length]
        output_sequence = inputArray[i + sequence_length]
        input_data.append(input_sequence)
        output_data.append(output_sequence)

    input_data = numpy.asarray(input_data)
    output_data = numpy.asarray(output_data)

    return (input_data, output_data)

data,target = shapeData(sequence_length)
print("DATA"+str(data.shape))
print("TARGET"+str(target.shape))

text_file = open("data2.txt", "w")
text_file.write(json.dumps(data.tolist(), indent=2))
text_file.close()

print("inputArray",inputArray.shape)
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


model.fit(x_train, y_train, batch_size=32, epochs=200)
score = model.evaluate(x_train, y_train, batch_size=32)

actualTrain = x_train[0]
result = numpy.empty([1, 88])
for x in range(0,20):
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



