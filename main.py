import cv2 
from cvzone import HandTrackingModule as htm
import keyboard as K
import cvzone as cz

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720) # HD resolution

detector = htm.HandDetector(maxHands=1, detectionCon=0.7)
myButton = K.Button([10, 80])
butt = myButton.keys()

fpsReader = cz.FPS()
#txt = ''

if cap.isOpened() == False:
    print('Cannot open video stream')

while True:
    ret, frame = cap.read()

    # find hand landmarks
    img = detector.findHands(cv2.flip(frame, 1))
    lmst, bboxInfo = detector.findPosition(img)
    img = myButton.draw(img, outline="std")
    #area = bboxInfo['bbox']

    if len(lmst):
        l,_,_, = detector.findDistance(8, 12, img, False)
        fingers = detector.fingersUp()
        _, text = myButton.type(img, lmst, fingers, l)
        #txt += text
        
    # cv2.rectangle(img,(10,570),(790,640),(150,0,0),cv2.FILLED)
    # cv2.putText(img,txt, (20, 630), 
    #                   cv2.FONT_HERSHEY_PLAIN, 5,(225,225,225),5)

    fps, img = fpsReader.update(img, (10,50),(0,0,0), 2, 2)
    
    if ret == True:
        cv2.imshow('Frame', img)

        if cv2.waitKey(25) & 0xFF == 27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
