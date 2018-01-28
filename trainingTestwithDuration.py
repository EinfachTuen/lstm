# -*- coding: utf-8 -*-
#Diese Datei kümmert sich um das erstellen und trainieren
#der jeweiligen models.
#Die Models werden als h5-Models gespeichert und dann
#von modelPredictionWithDuration.py benutzt

import numpy as numpy

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt

import json
import requestTests
import os

#Initialisierung wichtiger Variablen
epochen = 100
sequence_length = 30
batch_size = 2740
hl_Neuronen_Noten = 256
hl_Neuronen_Duration = 155

#Bringt die Input- und Output-Daten in eine
#für das Netz passende Forme
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

#Erstellt ein h5-Model, das zur Generierung der
#Duration von Noten benutzt werden kann
#Dazu wird zuerst ein neues LSTM erstellt und
#mit den Input- und Output-Daten trainiert.
def durationModel(notes,channelName,folderName,hl_Neuronen,sequence_length,epochen,batch_size):

    #Initialisierung wichtiger Variablen
    #'target' wird hier nicht gebraucht
    uploadResult = numpy.asarray(notes, dtype=numpy.float32)
    data, target, duration = shapeData(uploadResult, sequence_length)
    x_train = data


    #Erstellung des Models
    duration_model = Sequential()
    duration_model.add(LSTM(129, input_shape=(sequence_length, uploadResult.shape[1])))
    duration_model.add(Dense(1))
    duration_model.compile(loss='mean_absolute_error', optimizer='adam')

    #Logging
    numpy.savetxt("./models/"+folderName+'/'+str(channelName)+"_x2Train.txt", x_train[0], fmt='%.3f')
    numpy.savetxt("./log/"+str(channelName)+"_duration.txt", duration, fmt='%.3f')

    #Training
    history =duration_model.fit(x_train, duration, batch_size=batch_size, epochs=epochen)
    duration_model.evaluate(x_train, duration, batch_size=batch_size)

    #Speicherung des Models
    duration_model.save('./models/'+folderName+'/'+str(channelName)+'_durationsModel.h5')
    return history

#Erstellt ein h5-Model, das zur Noten-Generierung
#benutzt werden kann.
#Dazu wird zuerst ein neues LSTM erstellt und
#mit den Input- und Output-Daten trainiert.
def createModelForChannel(notes,channelName,folderName,hl_Neuronen,sequence_length,epochen,batch_size):

    #Initialisierung wichtiger Variablen
    uploadResult = numpy.asarray(notes, dtype=numpy.float32)
    data,target,duration = shapeData(uploadResult,sequence_length)
    x_train = data
    y_train = numpy.asarray(target)

    # Logging
    numpy.savetxt("./log/" + str(channelName) + "_x2Train.txt", x_train[0], fmt='%.3f')
    numpy.savetxt("./log/" + str(channelName) + "_duration.txt", duration, fmt='%.3f')
    numpy.savetxt("./log/newTest.txt", uploadResult, fmt='%.3f')

    #Erstellung des Models
    model = Sequential()
    model.add(LSTM(129, input_shape=(sequence_length,uploadResult.shape[1])))
    model.add(Dense(128, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

    #Logging
    numpy.savetxt("./log/"+str(channelName)+"_x2Train.txt",x_train[0],fmt='%.3f')
    numpy.savetxt("./log/"+str(channelName)+"_duration.txt",duration,fmt='%.3f')

    #Training
    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochen)
    #score = model.evaluate(x_train, y_train, batch_size=batch_size)

    #Speichern des h5-Models
    model.save('./models/'+folderName+'/'+str(channelName)+'_noteModel.h5')
    return history

#Erstellt ein h5-Model, das zur Noten-Generierung
#benutzt werden kann.
#Dazu wird zuerst ein neues LSTM erstellt und
#mit den Input- und Output-Daten trainiert.
#Die Input/Output-Daten werden mithilfe des
#Parameters 'notes' ermittelt
#Zusätzlich enthält das Netz noch einen
#LSTM hidden-Layer mit 'hl_Neuronen' Neuronen
def createModelForChannelDuoLSTM(notes,channelName,folderName,hl_Neuronen,sequence_length,epochen,batch_size):

    #Initialisierung wichtiger Variablen
    uploadResult = numpy.asarray(notes, dtype=numpy.float32)
    data,target,duration = shapeData(uploadResult,sequence_length)
    x_train = data
    y_train = numpy.asarray(target)

    # Logging
    numpy.savetxt("./log/" + str(channelName) + "_x2Train.txt", x_train[0], fmt='%.3f')
    numpy.savetxt("./log/" + str(channelName) + "_duration.txt", duration, fmt='%.3f')
    numpy.savetxt("./log/newTest.txt", uploadResult, fmt='%.3f')

    #Erstellung des Models
    model = Sequential()
    model.add(LSTM(129, input_shape=(sequence_length,uploadResult.shape[1]), return_sequences=True))
    model.add(LSTM(hl_Neuronen))
    model.add(Dense(128, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

    #Logging
    numpy.savetxt("./log/"+str(channelName)+"_x2Train.txt",x_train[0],fmt='%.3f')
    numpy.savetxt("./log/"+str(channelName)+"_duration.txt",duration,fmt='%.3f')

    #Training
    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochen,verbose=1)
    #score = model.evaluate(x_train, y_train, batch_size=batch_size)

    #Speichern des h5-Models
    model.save('./models/'+folderName+'/'+str(channelName)+'_noteModel.h5')
    return history

#Erstellt ein h5-Model, das zur Generierung der
#Duration von Noten benutzt werden kann
#Dazu wird zuerst ein neues LSTM erstellt und
#mit den Input- und Output-Daten trainiert.
#Zusätzlich enthält das Netz noch einen
#LSTM hidden-Layer mit 'hl_Neuronen' Neuronen
def durationModelDuoLSTM(notes,channelName,folderName,hl_Neuronen,sequence_length,epochen,batch_size):

    #Initialisierung wichtiger Variablen
    #'target' wird hier nicht gebraucht
    uploadResult = numpy.asarray(notes, dtype=numpy.float32)
    data, target, duration = shapeData(uploadResult, sequence_length)
    x_train = data


    #Erstellung des Models
    duration_model = Sequential()
    duration_model.add(LSTM(129, input_shape=(sequence_length, uploadResult.shape[1]), return_sequences=True))
    duration_model.add(LSTM(hl_Neuronen))
    duration_model.add(Dense(1))
    duration_model.compile(loss='mean_absolute_error', optimizer='adam')

    #Logging
    numpy.savetxt("./models/"+folderName+'/'+str(channelName)+"_x2Train.txt", x_train[0], fmt='%.3f')
    numpy.savetxt("./log/"+str(channelName)+"_duration.txt", duration, fmt='%.3f')

    #Training
    history = duration_model.fit(x_train, duration, batch_size=batch_size, epochs=epochen,verbose=1)
    #score = duration_model.evaluate(x_train, duration, batch_size=batch_size)

    #Speicherung des Models
    duration_model.save('./models/'+folderName+'/'+str(channelName)+'_durationModel.h5')
    return history


#Plottet den Verlauf vom loss des Models
#'history': Training des Models gibt ein
#history-object zurück, das hier als
#Eingabe verwendet wird
def printHistory(history):
    print(history.history.keys())
    plt.plot(history.history['loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

#Erstellen der Ordner in denen die Models gespeichert werden
uploadResult = requestTests.GetNotesPlusFloatDuration()
folderName = uploadResult["folder"]
midiEvents = uploadResult["notes"]
if not os.path.exists("./models/"+folderName):
    os.makedirs("./models/"+folderName)

#Erstellen und Trainieren der Netze,
#sowie die Speicherung ihrer jeweiligen, und printing des model losses als graph
#h5-Models
item = 0
for channel in midiEvents:
    printHistory(createModelForChannelDuoLSTM(midiEvents[item]["notes"],midiEvents[item]["channel"],folderName, hl_Neuronen_Noten, sequence_length, epochen, batch_size))
    printHistory(durationModelDuoLSTM(midiEvents[item]["notes"],midiEvents[item]["channel"], folderName, hl_Neuronen_Duration, sequence_length, epochen, batch_size))

    item = item + 1


