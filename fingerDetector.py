import cv2
import time
import os
import handTrackingModule as hdm

wCam, hCam = 1020, 850

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "hands"   # Here your Directory file name (the pictures should be posted here)
myList = os.listdir(folderPath)
print(myList)

overlay = []
for imPath in myList:
    image = cv2.imread(f"{folderPath}/{imPath}")
    #print(f"{folderPath}/{imPath}")
    overlay.append(image)
print(len(overlay))
pTime = 0
detector = hdm.handDetection(detectionCon=0.75)
tipID = [4, 8, 12, 16, 20]


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)

    if len(lmList) != 0:
        fingers = []
        # Bosh marmoq

        if lmList[tipID[0]][1] > lmList[tipID[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 barmoqlar

        for id in range(0, 5):
            if lmList[tipID[id]][2] < lmList[tipID[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        #print(fingers)
        fingerscount = fingers.count(1)
        print(fingerscount)

        h, w, c = overlay[fingerscount - 1].shape
        img[0:h, 0:w] = overlay[fingerscount - 1]

        # cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        # cv2.putText(img, str(fingerscount), (45, 375), cv2.FONT_HERSHEY_PLAIN,
        #             10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



