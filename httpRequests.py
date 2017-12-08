import requests

file_ = {'file': ('fp-1all.mid', open('fp-1all.mid', 'rb'))}
r = requests.post("http://flashmusicgames.com/midi/mid2txt.php", params={'mid_upload': file_, 'tt': 0, 'MAX_FILE_SIZE':1048576},headers ={'content-type': 'multipart/form-data; boundary=--f8c266cf436941019c5a80c7d4779a57'})
print(r.status_code, r.reason)
print(r.text)