import sys
import cv2 
from cvzone.HandTrackingModule import HandDetector

from keyboard import keyboard

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720) # HD resolution

detector = HandDetector(maxHands=1, detectionCon=0.7)
_keyboard = keyboard([20, 40])

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

        img = _keyboard.draw(img, style='std')

    if landmarks:
        fingers = detector.fingersUp(hand)
        lenght, info, img = detector.findDistance(landmarks[8][:2], landmarks[12][:2], img)
        _, text = _keyboard.click(img, landmarks, fingers, lenght)
    
    # #area = bboxInfo['bbox']

    # fps, img = fpsReader.update(img, (10,50),(0,0,0), 2, 2)
    
    cv2.imshow('Frame', img)

    if cv2.waitKey(25) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
