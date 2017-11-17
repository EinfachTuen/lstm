# -*- coding: utf-8 -*-
import numpy as numpy


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
    
print(createInputArray())
        
    
    
        
    