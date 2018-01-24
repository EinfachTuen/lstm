#Diese Datei kümmert sich um die Generierung der neuen Musik.
#Dazu wird das in midiTraining.py erstellte h5-model benutzt.
import numpy as numpy

from keras.models import load_model

import json
import midiConverter

#Laden des in midiTraining.py erstellten Models
model = load_model('my_modelDoubleLstm.h5')


actualTrain = numpy.loadtxt("xTrain.txt")

#Initialisierung eines leeren ResultArrays
result = numpy.empty([1, 88])
NotesToGenerate = 5000

#Generierung eines ResultArrays 'result' (shape: (NotesToGenerate, 88))
#das die Wahrscheinlichkeiten der einzelnen Noten zu den jeweilige Zeitschritten enthält
#result[6][5] enthält also die Wahrscheinlichkeit, dass im sechsten Zeitschritt die
#Note '5' gespielt wird
for x in range(0,NotesToGenerate):
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
print("finished saves now")

#"Glättung" der Ergebnisse in 'result'
#Wahrscheinlichkeiten >0.5 werden zu 1
#Wahrscheinlichkeiten <0.5 werden zu 0
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

#Konvertieren des Resultats in einen String,
#und dann vom String in eine Midi-Datei
finalString = midiConverter.convertToMidiTrack(result)
print(finalString)
text_file = open("result55.txt", "w")
text_file.write(json.dumps(finalString, indent=2))
text_file.close()
uploadResult = midiConverter.getMidiFromText(finalString,"testPyDoubleLstm120E")
print(uploadResult+".mid")



