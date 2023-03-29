import cv2
import htm
import autopy
import numpy as np

wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector()
wScr, hScr = autopy.screen.size()
br = 0
while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList,bbox = detector.findPosition(img,draw= True)
        #print(lmList)

        if len(lmList) != 0:
            fingers = detector.fingersUp()
            # print(fingers)
            totalFingers = fingers.count(1)
            # print(totalFingers)

            cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)

            if totalFingers == 1:
                while True:
                    # 1. Find hand Landmarks
                    success, img = cap.read()
                    img = detector.findHands(img)
                    lmList, bbox = detector.findPosition(img)
                    # 2. Get the tip of the index and middle fingers
                    if len(lmList) != 0:
                        x1, y1 = lmList[8][1:]
                        x2, y2 = lmList[12][1:]
                        # print(x1, y1, x2, y2)

                        # 3. Check which fingers are up
                        fingers = detector.fingersUp()
                        # print(fingers)
                        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                                      (255, 0, 255), 2)
                        # 4. Only Index Finger : Moving Mode
                        if fingers[1] == 1 and fingers[2] == 0:
                            # 5. Convert Coordinates
                            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                            # 6. Smoothen Values
                            clocX = plocX + (x3 - plocX) / smoothening
                            clocY = plocY + (y3 - plocY) / smoothening

                            # 7. Move Mouse
                            autopy.mouse.move(wScr - clocX, clocY)
                            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
                            plocX, plocY = clocX, clocY

                        # 8. Both Index and middle fingers are up : Clicking Mode
                        if fingers[1] == 1 and fingers[2] == 1:
                            # 9. Find distance between fingers
                            length, img, lineInfo = detector.findDistance(8, 12, img)
                            #print(length)
                            # 10. Click mouse if distance short
                            if length < 40:
                                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                                           15, (0, 255, 0), cv2.FILLED)
                                autopy.mouse.click()

                    # 12. Display

                    cv2.imshow("Image", img)
                    cv2.waitKey(1)

            if totalFingers == 0:
                import Volume


            else:
                cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)


        cv2.imshow("Image", img)
        cv2.waitKey(1)
