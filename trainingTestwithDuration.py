# -*- coding: utf-8 -*-
import numpy as numpy

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop

import json
import requestTests

epochen = 100
sequence_length = 1

def shapeData(uploadResult,sequence_length):
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

def durationModel(x_train,uploadResult,duration,data,item,channelName):
    duration_model = Sequential()
    duration_model.add(LSTM(129, input_shape=(sequence_length, uploadResult.shape[1])))
    duration_model.add(Dense(1))
    duration_model.compile(loss='mean_absolute_error', optimizer='adam')

    numpy.savetxt("./log/"+str(channelName)+"_x2Train.txt", x_train[0], fmt='%.3f')
    numpy.savetxt("./log/"+str(channelName)+"_duration.txt", duration, fmt='%.3f')
    duration_model.fit(data, duration, batch_size=64, epochs=epochen)
    score = duration_model.evaluate(data, duration, batch_size=64)
    duration_model.save('./models/'+str(channelName)+'_durationsModel.h5')

def createModelForChannel(notes,channelName):
    uploadResult = numpy.asarray(notes, dtype=numpy.float32)

    numpy.savetxt("./log/newTest.txt", uploadResult, fmt='%.3f')
    print(uploadResult.shape)

    print(uploadResult.shape)


    data,target,duration = shapeData(uploadResult,sequence_length)
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
    numpy.savetxt("./log/"+str(channelName)+"_x2Train.txt",x_train[0],fmt='%.3f')
    numpy.savetxt("./log/"+str(channelName)+"_duration.txt",duration,fmt='%.3f')
    model.fit(x_train, y_train, batch_size=64, epochs=epochen)
    score = model.evaluate(x_train, y_train, batch_size=64)
    model.save('./models/'+str(channelName)+'_noteModel.h5')
    durationModel(x_train,uploadResult, duration, data, item, channelName)

uploadResult = requestTests.GetNotesPlusFloatDuration()
print(uploadResult[0]["channel"])
item = 0
for channel in uploadResult:
    createModelForChannel(uploadResult[item]["notes"],uploadResult[item]["channel"])
    item = item + 1



