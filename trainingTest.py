# -*- coding: utf-8 -*-
import numpy as numpy

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop

import json
import requestTests


uploadResult = requestTests.getMidiAsArray()
sequence_length = 100

def shapeData(sequence_length):
    input_data = []
    output_data = []

    for i in range(0, (uploadResult.shape[0] - sequence_length), 1):
        input_sequence = uploadResult[i:i + sequence_length]
        output_sequence = uploadResult[i + sequence_length]
        input_data.append(input_sequence)
        output_data.append(output_sequence)

    input_data = numpy.asarray(input_data)
    output_data = numpy.asarray(output_data)

    return (input_data, output_data)

data,target = shapeData(sequence_length)
print("DATA"+str(data.shape))
print("TARGET"+str(target.shape))

print("inputArray",uploadResult.shape)
print("target shape " +str(target.shape))
print(target)


print(data.shape)
model = Sequential()
model.add(LSTM(127, input_shape=(sequence_length,uploadResult.shape[1])))
model.add(Dense(127, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

x_train = data
y_train = numpy.asarray(target)
print("x2_train"+str(x_train.shape))
print("y2_train"+str(y_train.shape))

numpy.savetxt("./log/x2Train.txt",x_train[0],fmt='%i')
model.fit(x_train, y_train, batch_size=32, epochs=5)
score = model.evaluate(x_train, y_train, batch_size=32)

model.save('./models/my_model_new.h5')