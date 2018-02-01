import prediction

'''
Type here the Folder and Channel name of the model you like to run the prediction for.
'''
channel_name = 73
folder_Name = "bachOneChannel"
midiFileName = prediction.runPrediction(folder_Name,channel_name,str(channel_name)+"_"+folder_Name)
print(midiFileName)