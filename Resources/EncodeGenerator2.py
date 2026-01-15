import os
import cv2
import face_recognition

folderPath = '/Users/sreelakshmi/Desktop/VotingDetectorSystem/Images'
pathList = [filename for filename in os.listdir(folderPath) if not filename.startswith('.')]
print(pathList)

imgList = []
voterIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    voterIds.append(os.path.splitext(path)[0])

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
print(encodeListKnown)
print("Encoding is Completed")

