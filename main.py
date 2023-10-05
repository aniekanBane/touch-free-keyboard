import sys
import cv2 
from cvzone.HandTrackingModule import HandDetector

import keyboard as K

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720) # HD resolution

detector = HandDetector(maxHands=1, detectionCon=0.7)
myButton = K.Button([10, 80])
butt = myButton.keys()

# fpsReader = cz.FPS()

if not cap.isOpened():
    print('Cannot open video stream')
    sys.exit(1)

while True:
    ret, frame = cap.read()

    if not ret:
        print('Cannot read video stream')
        break

    cv2.flip(frame, 1, frame)

    # find hand landmarks
    hands, img = detector.findHands(frame, flipType=False)
    hand, landmarks, bbox = None, None, None
    if hands:
        hand = hands[0]
        landmarks = hand['lmList']
        bbox = hand['bbox']

        img = myButton.draw(img, outline="std")

    if landmarks:
        fingers = detector.fingersUp(hand)
        lenght, info, img = detector.findDistance(landmarks[8][:2], landmarks[12][:2], img)
        _, text = myButton.type(img, landmarks, fingers, lenght)
    
    # #area = bboxInfo['bbox']
        
    # cv2.rectangle(img,(10,570),(790,640),(150,0,0),cv2.FILLED)
    # cv2.putText(img,txt, (20, 630), 
    #                   cv2.FONT_HERSHEY_PLAIN, 5,(225,225,225),5)

    # fps, img = fpsReader.update(img, (10,50),(0,0,0), 2, 2)
    
    cv2.imshow('Frame', img)

    if cv2.waitKey(25) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
