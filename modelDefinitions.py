# -*- coding: utf-8 -*-
#Diese Datei kümmert sich um das erstellen und trainieren
#der jeweiligen models.
#Die Models werden als h5-Models gespeichert und dann
#von modelPredictionWithDuration.py benutzt

import numpy as numpy

from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.layers import Input, LSTM, Dense, Dropout
from keras.models import Model
from keras.utils import to_categorical

#Initialisierung wichtiger Variablen
epochen = 10
sequence_length = 15
batch_size = 200
hl_firstLSTM = 131
hl_secondLSTM = 256
hl_Neuronen_Noten = 256
hl_Neuronen_Duration = 155

#Diese Function Categorisiert alle Durations und Zeiten
def categorieze(duration):
    durationArrayNeu = []
    durationValues = set([])
    for value in duration:
        durationValues.add(value)
        i = 0
        for categorie in durationValues:
            if (categorie == value):
                durationArrayNeu.append(i)
            i = i + 1
        print(value)
    print("duration Categories" + str(durationArrayNeu))
    durationArrayNeu = numpy.asarray(durationArrayNeu)
    return (durationArrayNeu,durationValues)

#Bringt die Input- und Output-Daten in eine
#für das Netz passende Forme
def shapeData(uploadResult,sequence_length):
    input_data = []
    output_data = []
    output_duration = []
    output_time = []
    for i in range(0, (uploadResult.shape[0] - sequence_length), 1):
        input_sequence = uploadResult[i:i + sequence_length]
        output_sequence = uploadResult[i + sequence_length]
        input_data.append(input_sequence)
        output_data.append(output_sequence[:-2])
        output_duration.append(output_sequence[128])
        output_time.append(output_sequence[129])

    input_data = numpy.asarray(input_data)
    output_data = numpy.asarray(output_data)
    output_duration = numpy.asarray(output_duration)
    output_time = numpy.asarray(output_time)

    return (input_data, output_data,output_duration,output_time)

#Definition of the actual used model
def specialModel(notes,channelName,folderName,sequence_length,epochen,batch_size,hl_firstLSTM,hl_secondLSTM):
    #Initialisierung wichtiger Variablen
    uploadResult = numpy.asarray(notes, dtype=numpy.float32)
    print("uploadResult" + str(uploadResult.shape))
    if uploadResult.shape[0] > 13000:
        sequence_length = 4
    data,target,duration,time = shapeData(uploadResult,sequence_length)
    x_train = numpy.asarray(data)
    y_train = numpy.asarray(target)

    duration,durationValues = categorieze(duration)
    time,timeValues = categorieze(time)
    duration = to_categorical(duration)
    time = to_categorical(time)
    durationAmount = len(duration[0])
    timeAmount = len(time[0])
    durationValues =numpy.asarray(list(durationValues))
    timeValues =numpy.asarray(list(timeValues))

    print("Time"+ str(time.shape))
    print(timeAmount)
    print("duration"+ str(duration.shape))
    print(durationAmount)

    sequenceNo = 0

    print(str(duration.shape))
    # Logging
    print(str(x_train[0].shape))
    numpy.savetxt('./models/'+folderName+'/'+str(channelName) + "_duration_categories.txt", durationValues, fmt='%.3f')
    numpy.savetxt('./models/'+folderName+'/'+str(channelName) + "_time_categories.txt", timeValues, fmt='%.3f')
    numpy.savetxt('./models/' + folderName + '/' + str(channelName) + "_Notes.txt", x_train[0], fmt='%.3f')

    #Erstellung des Models
    mainInput = Input(shape=(sequence_length, uploadResult.shape[1]), dtype='float32', name='mainInput')
    print(mainInput)
    mainLSTM = LSTM(hl_firstLSTM, return_sequences=True)(mainInput)
    dropOut = Dropout(0.2)(mainLSTM)
    secondLSTM = LSTM(hl_secondLSTM)(dropOut)
    dropOut2 = Dropout(0.2)(secondLSTM)
    noteDenseLayer = Dense(128, activation='softmax', name='noteDenseLayer')(dropOut2)
    durationDenseLayer = Dense(durationAmount, name='durationDenseLayer',activation='softmax')(dropOut2)
    timeDenseLayer = Dense(timeAmount, name='timeDenseLayer',activation='softmax')(dropOut2)

    model = Model(inputs= mainInput, outputs=[noteDenseLayer, durationDenseLayer,timeDenseLayer])
    model.compile(optimizer='Adadelta',
                  loss={'noteDenseLayer': 'categorical_crossentropy', 'durationDenseLayer': 'categorical_crossentropy', 'timeDenseLayer': 'categorical_crossentropy'},metrics=['accuracy'])
    #Training
    history = model.fit(x_train, [y_train,duration,time], batch_size=batch_size, epochs=epochen, verbose=2, shuffle= False)
    #score = model.evaluate(x_train, y_train, batch_size=batch_size)
    print(history)
    #Speichern des h5-Models
    model.save('./models/'+folderName+'/'+str(channelName)+'_noteModel.h5')
    print(model.summary())
    return history


## Older Models
'''
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
    model.add(LSTM(hl_firstLSTM, input_shape=(sequence_length,uploadResult.shape[1]), return_sequences=True))
    model.add(LSTM(hl_secondLSTM))
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
'''

## Model definiton as experiment with channels but the necessary import methods are not here at the moment
'''
def allChannelsWithTimeModel(notes,channelName,folderName):

    #Initialisierung wichtiger Variablen
    uploadResult = numpy.asarray(notes, dtype=numpy.float32)
    data,target,duration,time = shapeData(uploadResult,sequence_length)
    x_train = numpy.asarray(data)
    y_train = numpy.asarray(target)
    sequenceNo = 0

    print(str(duration.shape))
    # Logging
    print(str(x_train[0].shape))
    numpy.savetxt("./models/"+folderName+'/'+str(channelName)+"_x2Train.txt", x_train[0], fmt='%.3f')
    numpy.savetxt("./log/" + str(channelName) + "_duration.txt", duration, fmt='%.3f')
    numpy.savetxt("./log/newTest.txt", uploadResult, fmt='%.3f')

    #Erstellung des Models
    mainInput = Input(shape=(sequence_length, uploadResult.shape[1]), dtype='float32', name='mainInput')
    print(mainInput)
    mainLSTM = LSTM(hl_firstLSTM, return_sequences=True)(mainInput)
    secondLSTM = LSTM(hl_secondLSTM)(mainLSTM)
    noteDenseLayer = Dense(128, activation='softmax', name='noteDenseLayer')(secondLSTM)
    durationDenseLayer = Dense(1, name='durationDenseLayer')(secondLSTM)
    timeDenseLayer = Dense(1, name='timeDenseLayer')(secondLSTM)

    model = Model(inputs= mainInput, outputs=[noteDenseLayer, durationDenseLayer,timeDenseLayer])
    model.compile(optimizer='Adadelta',
                  loss={'noteDenseLayer': 'categorical_crossentropy', 'durationDenseLayer': 'mean_absolute_error', 'timeDenseLayer': 'mean_absolute_error'})
    #Training
    history = model.fit(x_train, [y_train,duration,time], batch_size=batch_size, epochs=epochen, verbose=2)
    #score = model.evaluate(x_train, y_train, batch_size=batch_size)

    #Speichern des h5-Models
    model.save('./models/'+folderName+'/'+str(channelName)+'_noteModel.h5')
    print(model.summary())
    return history
'''





