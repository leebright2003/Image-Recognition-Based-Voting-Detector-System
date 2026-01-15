import os
import pickle

import cv2
import face_recognition

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://votingdetectorsystem-default-rtdb.firebaseio.com/",
    'storageBucket' : "votingdetectorsystem.appspot.com"
})

# Importing Voters Images
folderPath = "Images"
pathList = [filename for filename in os.listdir(folderPath) if not filename.startswith('.')]
print(pathList)

imgList = []
voterIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    voterIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(voterIds)

def findEncodings(imagesList):
    encodeList=[]
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding is Started...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, voterIds]
#print(encodeListKnown)
print("Encoding is Completed")

file = open("EncodedImageFile.p","wb")
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("Encoded File Saved")
