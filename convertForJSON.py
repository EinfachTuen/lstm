import numpy as numpy
import json as json

actualTrain = numpy.loadtxt("./log/25_x2Train.txt")
actualTrain = actualTrain.tolist()
text_file = open("./forJS/inputVektor.json", "w")
text_file.write(json.dumps(actualTrain, indent=2))
text_file.close()
