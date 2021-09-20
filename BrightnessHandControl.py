import cv2
import time
from matplotlib.pyplot import draw
import numpy as np
import handTrackingModule as htm
import math
import screen_brightness_control as sbc

wCam , hCam = 640 , 480

cap = cv2.VideoCapture(0)
cap.set(4 , wCam)
cap.set(3 , hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.8)
#get current brightness value
#print(sbc.get_brightness())
 
#set brightness to 50%
#  sbc.set_brightness()
 
#print(sbc.get_brightness())

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmsList = detector.findPosition(img,draw=False)
    if len(lmsList)!=0:
        #print(lmsList[4], lmsList[20])
        x1 , y1 = lmsList[4][1], lmsList[4][2]
        x2 , y2 = lmsList[20][1], lmsList[20][2]
        cx , cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img, (x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        print(length)

        new_brightness = np.interp(length, (30,200), (0,100))
            
        currentBrightness = sbc.get_brightness()

        threshold = 10

        if abs(currentBrightness - new_brightness) >= threshold:
                sbc.set_brightness(new_brightness)

        if length<50:
            cv2.circle(img,(cx,cy),15,(255,255,255),cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img,f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 1,
                    (255,255,255), 2)

    cv2.imshow("Volume/BrightnessControl",img)
    cv2.waitKey(1)