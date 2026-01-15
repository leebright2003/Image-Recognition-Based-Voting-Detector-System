import os

import cv2

folderPath = '/Users/sreelakshmi/Desktop/VotingDetectorSystem/Images'
modePathList = os.listdir(folderPath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderPath, path)))
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
voterIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))

    voterIds.append(os.path.splitext(path)[0])
    #print(path)
    #print(os.path.splitext(path)[0])
print(voterIds)
