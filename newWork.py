import cv2
import os
import pickle
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://votingdetectorsystem-default-rtdb.firebaseio.com/",
    'storageBucket' : "votingdetectorsystem.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)



imgBackground = cv2.imread('Resources/background.png')
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

#Loading the EncodedImageFile
print("Loading Encoded File ....")
file = open("EncodedImageFile.p","rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, voterIds = encodeListKnownWithIds
#print(voterIds)
print("Encoded File is loaded")


modeType = 1
counter = 0
id = -1

while True:
    success, img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS,faceCurrentFrame)


    imgBackground[162:162 + 480, 55:55 +640] = img
    imgBackground[44:44 + 633,808:808 +414] = imgModeList[modeType]
    cv2.waitKey(1)

    if faceCurrentFrame:
        for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches",matches)
            # print("faceDis",faceDistance)

            matchIndex = np.argmin(faceDistance)
            # print("Match Index",matchIndex)

            if matches[matchIndex]:
                # print("Known Face is Detected")
                # print(voterIds[matchIndex])
                y1, x2, y2, x1 = faceLocation
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = voterIds[matchIndex]
                # print(id)
                if counter == 0:
                    counter = 1
                    modeType = 2
            else:
                cvzone.putTextRect(imgBackground, "Unknown Face", (175, 600))
                cv2.waitKey(1)
                print("Unknown Face is Detected")

        if counter != 0:

            if counter == 1:
                voterInfo = db.reference(f'Voters/{id}').get()
                print(voterInfo)
                # Get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # Update the voting of the voter
                datetimeObject = datetime.strptime(voterInfo['voting_time'], "%Y-%m-%d %H:%M:%S")

                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                #print(secondsElapsed)
                if secondsElapsed > 2600:
                    ref = db.reference(f'Voters/{id}')
                    voterInfo['voting_done'] += 1
                    ref.child('voting_done').set(voterInfo['voting_done'])
                    ref.child('voting_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    #if voterInfo['voting_done'] == 0 or voterInfo['voting_done'] == 1:
                        #print(voterInfo)
                else:
                    modeType = 4
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 4:

                if 10 < counter < 20:
                    modeType = 3

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(voterInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    (w, h), _ = cv2.getTextSize(voterInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(voterInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                    cv2.waitKey(1)

            counter += 1

            if counter >= 20:
                counter = 0
                modeType = 1
                voterInfo = []
                imgStudent = []
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType=1
        counter=0

    cv2.imshow("Voting Detector",imgBackground)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()