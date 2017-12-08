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

import KTimage as kt


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
    notenArray = numpy.zeros(2037, dtype=numpy.int)
    timeStep = 120
    midiStartString = """MFile 1 17 480
MTrk
0 Meta TrkName "untitled"
0 SMPTE 96 0 3 0 0
0 TimeSig 4/4 24 8
0 KeySig 0 major
0 Tempo 600000
0 Meta Marker "A"
34560 Meta Marker "1."
36480 Meta Marker "A'"
71040 Meta Marker "2."
72960 Meta Marker "B"
123840 Tempo 1200000
123840 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Solo Flute"
0 PrCh ch=1 p=73
0 Par ch=1 c=7 v=100
0 Par ch=1 c=10 v=64"""
    Ende = """124800 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Johann Sebastian Bach  (1685-1750)"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Partita in A minor for Solo Flute - BWV 1013"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "1st Movement: Allemande"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Sequenced with Cakewalk Pro Audio by"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "David J. Grossman - dave@unpronounceable.com"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "This and other Bach MIDI files can be found at:"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Dave's J.S. Bach Page"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "http://www.unpronounceable.com/bach"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Original Filename: fp-1all.mid"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Last Modified: March 1, 1997"
0 Meta TrkEnd
TrkEnd"""    
    
    #notenArray fuellen, notenArray[i] = Note, die zum Zeitpunkt i aktiv ist
    #falls notenArray[i] == 0, werden die Noten deaktiviert
    #man beachte: Zeitpunkt wird nur alle zwei i's inkrementiert
    #Zeitpunkt(i=1) = 0
    #Zeitpunkt(i=2) = 120
    #Zeitpunkt(i=3) = 120
    #Zeitpunkt(i=4) = 240 usw
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
            
    
    return midiStartString+""+NotePartMidiString+""+Ende
                
                
#   #text schreiben 
#    for i in range(0, notenArray.size-1):
#        if notenArray[i] == 0 & i == 0:
#            megaString = """%s
#%d On ch=1 n=0 v=0""" % (megaString, timeStep)        
#        if notenArray[i] == 0 & i != 0:
#            megaString = """%s
#%d On ch=1 n=%d v=0""" % (megaString, timeStep, notenArray[i-1])
#        if notenArray[i] != 0:
#            megaString = """%s
#%d On ch=1 n=%d v=100""" % (megaString, timeStep, notenArray[i])
#            timeStep = timeStep + 120
#    
#    megaString = """%s %s""" % (megaString, Ende)
#    
#    return megaString
    
    
    
    
    
    
    
    
    
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
optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

x_train = numpy.asarray(data)
y_train = numpy.asarray(target)


model.fit(x_train, y_train, batch_size=88, epochs=5)
score = model.evaluate(x_train, y_train, batch_size=88)
result = model.predict(x_train, batch_size=88)
#print(score)
#print(result)
endresult = result
i = 0

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



diggaString = convertToMidi(result)
print(diggaString)
text_file = open("result55.txt", "w")

text_file.write(diggaString)

text_file.close()
#numpy.savetxt("result55.txt",diggaString)


