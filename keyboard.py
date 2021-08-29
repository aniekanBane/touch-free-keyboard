"""
Touch free keyboard Module
By: Aniekan Umanah
version: 1.0
"""

import cv2
import time
from cvzone.Utils import cornerRect
from pynput.keyboard import Key, Controller

class Button(object):

    kys = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
           ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
           ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',';'],
           ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '?'],
           ['fn', 'ctrl', 'cmd', '', 'Enter']]

    keyboard = Controller()

    def __init__(self, pos):
        """
        The base class of the class hierachy\n
        :param pos: x, y coordinates of first key
        """
        self.pos = pos
        self.size = [72,72]
        self.button =[]
    
    def keys(self):
        """
        Assign each letter in kys an x, y cordinate and get the button size. 
        """
        x, y = self.pos
        w, h, = self.size
    
        self.button =[]
        self.boxlst = []
        for i in range(len(self.kys)):
            for key in self.kys[i]:
                self.button.append([key, x+10, y])
                x += 80
                if key == '':
                    x += 320
            x = self.pos[0]
            y += 80
        
        if len(self.button):
            for button in self.button:
                text, x1, y1 = button
                self.boxlst.append([text, x1, y1, w, h])

                if text == 'cmd':
                    w = 390
                if text == '':
                    w = 150

    def draw(self, img, color=(225,0,0), outline="std"):
        """
        display keyboard on the screen\n
        :param img: frame  to display on
        :param color: color of the keys
        :param outline: style of keyboard
        """
        if color[1] >= 150 and "md" not in outline:
            raise ValueError('color cannot have high value of green element, please choose another value')
        
        if self.boxlst != 0:
            for i in self.boxlst:
                text, x, y, w, h = i
                if "std" in outline:
                    cv2.rectangle(img, (x,y), (x+w, y+h), color, cv2.FILLED)
                
                if "md" in outline:
                    cv2.rectangle(img, (x-10, y), (x, y+h), color, cv2.FILLED)
                    cv2.rectangle(img, (x+w, y), (x+w+10, y+h), color, cv2.FILLED)
                      
                if "outln" in outline:
                    cornerRect(img, i[1:], 25, 3, colorR=color, colorC=(0,225,100))

                cv2.putText(img, text, TextPos(text,x,y,50), cv2.FONT_HERSHEY_PLAIN, 
                                        2, (225, 225, 255), cv2.LINE_4)

        return img
    
    def type(self, img, lndms, fingers, dist):
        """
        type characters if the index finger and middle finger are close\n
        :param img: frame to display on
        :param lndms: hand landmrks
        :param fingers: how many fingers are up
        :param dist: x-axis offset between two landmarks
        """
        txt = ''

        for i in self.boxlst:
            text, x, y, w, h = i
            if x < lndms[8][0] < x+w and y < lndms[8][1] < y+h:
                if fingers[1] == 1 and fingers[2] == 0:
                    #cv2.rectangle(img,(x,y), (x+w, y+h), (100,0,0), cv2.FILLED)
                    cv2.putText(img, text, TextPos(text,x,y,50), cv2.FONT_HERSHEY_PLAIN, 
                                                2, (225, 225, 255), cv2.LINE_4)
                    cv2.circle(img, (lndms[8]), 25, (0,0,0), 3, cv2.LINE_AA)

                elif fingers[1] == 1 and fingers[2] == 1:
                    if dist < 40:
                        #self.keyboard.press(text)
                        cv2.rectangle(img,(x,y), (x+w, y+h), (0,255,0), cv2.FILLED)
                        cv2.putText(img, text, TextPos(text,x,y,50), cv2.FONT_HERSHEY_PLAIN, 
                                                2, (225, 225, 255), cv2.LINE_4)
                        txt = Text(text)
                        self.keyboard.press(txt)
                        time.sleep(0.15)

        return img, txt
    
    #def DragKeyboard():

#cv2.getTextSize(text, fontFace, fontScale, thickness)          
     
def TextPos(text, x, y, l):
    """text positions in keys"""
    if text == 'fn':
        return (x+15, y+l)
    if text == 'ctrl':
        return (x+4, y+l)
    if text == 'cmd':
        return (x+2, y+l)
    if text == '':
        return (x+28, y+l)
    else:
        return (x+20, y+l)  

def Text(text):
    """button action"""
    if text == 'fn':
        return Key.shift
    if text == 'ctrl':
        return Key.ctrl
    if text == 'cmd':
        return Key.cmd
    if text == '':
        return Key.space
    if text == 'Enter':
        return Key.enter
    else:
        return text

# def Width(text, w):
#     if text == '':
#         return 390
#     if text == 'Enter':
#         return 150
#     else:
#         return w
     