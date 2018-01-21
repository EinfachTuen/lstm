# -*- coding: utf-8 -*-
import numpy as numpy

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop

import json
import requestTests


uploadResult = requestTests.GetNotesPlusFloatDuration()

print(uploadResult.shape)
epochen = 200
sequence_length = 50
print(uploadResult.shape)
def shapeData(sequence_length):
    input_data = []
    output_data = []
    output_duration = []
    for i in range(0, (uploadResult.shape[0] - sequence_length), 1):
        input_sequence = uploadResult[i:i + sequence_length]
        output_sequence = uploadResult[i + sequence_length]
        input_data.append(input_sequence)
        output_data.append(output_sequence[:-1])
        output_duration.append(output_sequence[128])

    input_data = numpy.asarray(input_data)
    output_data = numpy.asarray(output_data)
    output_duration = numpy.asarray(output_duration)

    return (input_data, output_data,output_duration)

data,target,duration = shapeData(sequence_length)
print("DATA"+str(data.shape))
print("TARGET"+str(target.shape))

print("inputArray",uploadResult.shape)
print("target shape " +str(target.shape))
print(target)


print(data.shape)
model = Sequential()
model.add(LSTM(129, input_shape=(sequence_length,uploadResult.shape[1])))
model.add(Dense(128, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

x_train = data
y_train = numpy.asarray(target)
print("x2_train"+str(x_train.shape))
print("y2_train"+str(y_train.shape))


numpy.savetxt("./log/x2Train.txt",x_train[0],fmt='%.3f')
numpy.savetxt("./log/duration.txt",duration,fmt='%.3f')
model.fit(x_train, y_train, batch_size=32, epochs=1)
score = model.evaluate(x_train, y_train, batch_size=32)
#model.save('./models/noteModel.h5')

def durationModel():
    duration_model = Sequential()
    duration_model.add(LSTM(129, input_shape=(sequence_length, uploadResult.shape[1])))
    duration_model.add(Dense(1))
    duration_model.compile(loss='mean_absolute_error', optimizer='adam')

    numpy.savetxt("./log/x2Train.txt", x_train[0], fmt='%.3f')
    numpy.savetxt("./log/duration.txt", duration, fmt='%.3f')
    duration_model.fit(data, duration, batch_size=32, epochs=epochen)
    score = duration_model.evaluate(data, duration, batch_size=32)
    duration_model.save('./models/durationsModel.h5')

durationModel()