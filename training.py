# -*- coding: utf-8 -*-
#Diese Datei kümmert sich um das erstellen und trainieren
#der jeweiligen models.
#Die Models werden als h5-Models gespeichert und dann
#von modelPredictionWithDuration.py benutzt


import matplotlib.pyplot as plt

import modelDefinitions
import apiCalls
import os


#Plottet den Verlauf vom loss des Models
#'history': Training des Models gibt ein
#history-object zurück, das hier als
#Eingabe verwendet wird
def printHistory(history,channelName):
    print(history.history.keys())
    plt.plot(history.history['loss'])
    plt.plot(history.history['noteDenseLayer_loss'])
    plt.plot(history.history['durationDenseLayer_loss'])
    plt.plot(history.history['timeDenseLayer_loss'])
    plt.plot(history.history['noteDenseLayer_acc'])
    plt.plot(history.history['durationDenseLayer_acc'])
    plt.plot(history.history['timeDenseLayer_acc'])
    plt.title('model loss channel:'+str(channelName))
    plt.ylabel('loss')
    plt.xlabel('epoch')
    axes = plt.gca()
    axes.set_ylim([0, 2])
    plt.legend(['Loss', 'Loss Note', 'Loss Duration','Loss Time','Accuracy Notes','Accuracy Durations','Accuracy Time'], loc='upper left')
    plt.show()

#Initialisierung wichtiger Variablen
epochen = 10
sequence_length = 15
batch_size = 200
hl_firstLSTM = 131
hl_secondLSTM = 256
hl_Neuronen_Noten = 256
hl_Neuronen_Duration = 155

# Erstellen der Ordner in denen die Models gespeichert werden
uploadResult = apiCalls.GetNotesPlusFloatDuration()
folderName = uploadResult["folder"]
midiEvents = uploadResult["notes"]
if not os.path.exists("./models/"+folderName):
    os.makedirs("./models/"+folderName)

# testVals = requestTests.GetAllTogether()
# folderName = testVals["folder"]
# midiEvents = testVals["notes"]
# if not os.path.exists("./models/"+folderName):
#     os.makedirs("./models/"+folderName)
# allChannelsWithTimeModel(midiEvents,folderName,folderName)
# Es muss der Webstormserver aktiv sein auf Localhost
# Erstellen und Trainieren der Netze,
# sowie die Speicherung ihrer jeweiligen, und printing des model losses als graph
# h5-Models
channel_iterator = 0
for channel in midiEvents:
    #Generate the model and print its History
    history =  modelDefinitions.specialModel(midiEvents[channel_iterator]["notes"], midiEvents[channel_iterator]["channel"], folderName, sequence_length, epochen, batch_size,hl_firstLSTM,hl_secondLSTM)
    printHistory(history,midiEvents[channel_iterator]["channel"])
    channel_iterator = channel_iterator + 1


