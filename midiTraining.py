# -*- coding: utf-8 -*-
import numpy as numpy

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop

import json
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

numpy.savetxt("xTrain.txt",x_train[0])
model.fit(x_train, y_train, batch_size=32, epochs=200)
score = model.evaluate(x_train, y_train, batch_size=32)

model.save('my_model.h5')