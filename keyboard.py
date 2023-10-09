"""
Touch free keyboard Module
By: Aniekan Umanah
version: 1.0
"""

import cv2
import time
from cvzone.Utils import cornerRect
from pynput.keyboard import Key, Controller


class keyboard:

    kys = (['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
           ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
           ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
           ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '?'],
           ['shift', 'ctrl', 'cmd', ' ', 'Enter'])

    controller = Controller()

    def __init__(self, pos: list):
        """
        Keyboard

        Args
        ----
        - pos: x, y coordinates of first key
        """

        self.pos = pos
        self.size = 70
        self._spacing = self.size // 10
        self.buttons = []

        self.__keys()

    def __keys(self):
        """
        Assign each letter in kys an x, y cordinate, and also the size of the button. 
        """
        x, y = self.pos
        w = h = self.size

        for row in self.kys:
            for key in row:
                self.buttons.append([key, x, y, w, h])
                w = self.size
                x += self._spacing + w

                if key == 'cmd':  # space bar
                    w += (w * 4) + (self._spacing * 4)

                if key.isspace():  # enter key
                    x += (w * 4) + (self._spacing * 4)
                    w += w + self._spacing
            x = self.pos[0]
            y += self._spacing + h

    def draw(self, img, color=(66, 43, 36), style='std'):
        """
        Display keyboard on the screen

        Args
        ----
        - img: frame  to display on
        - color: color of the keys
        - style: style of keyboard

        Return
        ------
        img: image with keyboard drawn
        """

        if color[1] >= 150 and style != 'bar':
            raise ValueError(
                'color cannot have high value of green element, please choose another value')

        if self.buttons:
            for i in self.buttons:
                text, x, y, w, h = i
                if style == 'std':
                    cv2.rectangle(img, (x, y), (x+w, y+h), color, cv2.FILLED)

                elif style == 'border':
                    cornerRect(img, i[1:], self.size // 3, 3, colorR=color, colorC=(96, 83, 151))

                elif style == 'bar':
                    cv2.rectangle(img, (x-self._spacing, y), (x, y+h), color, cv2.FILLED)
                    cv2.rectangle(img, (x+w, y), (x+w+self._spacing, y+h),
                                  color, cv2.FILLED)

                cv2.putText(img, text, TextPos(text, x, y, w, h), cv2.FONT_HERSHEY_PLAIN,
                            FONT_SCALE(text), (225, 225, 255), THICKNESS(text))

        return img

    def click(self, img, lndms, fingers, dist):
        """
        Select characters if the index finger and middle finger are close

        Args
        ----
        - img: frame to display on
        - lndms: hand landmrks
        - fingers: how many fingers are up
        - dist: x-axis offset between two landmarks

        Return
        ------
        - img: image
        - txt: the selected key
        """
        txt = ''

        for i in self.buttons:
            text, x, y, w, h = i
            if x < lndms[8][0] < x+w and y < lndms[8][1] < y+h:
                if fingers[1] == 1 and fingers[2] == 0:
                    # cv2.rectangle(img,(x,y), (x+w, y+h), (100,0,0), cv2.FILLED)
                    # cv2.putText(img, text, TextPos(text, x, y, w, h), cv2.FONT_HERSHEY_PLAIN,
                    #             2, (225, 225, 255), cv2.LINE_4)
                    cv2.circle(img, lndms[8][:2], self.size // 2, (0, 0, 0), 3, cv2.LINE_AA)

                elif fingers[1] == 1 and fingers[2] == 1:
                    if dist < 40:
                        cv2.rectangle(img, (x, y), (x+w, y+h),
                                      (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, text, TextPos(text, x, y, w, h), cv2.FONT_HERSHEY_PLAIN,
                                    FONT_SCALE(text), (225, 225, 255), THICKNESS(text))
                        txt = Text(text)
                        self.controller.press(txt)
                        time.sleep(0.05)

        return img, txt

    # def DragKeyboard(self, lndms, fingers):
    #      for i in self.boxlst:
    #          text, x, y, w, h = i
    #          if all(fingers):

FONT_SCALE = lambda text: 1 if len(text) > 1 else 2
THICKNESS = lambda text: 2 if len(text) > 1 else cv2.LINE_4

def TextPos(text, x, y, wi, he):
    """text positions in keys"""

    ((w, h), _) = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, FONT_SCALE(text), THICKNESS(text))
    a = (x+wi//2) - (w//2)
    b = (y+he//2) + (h//2)

    return (a, b)


def Text(text: str):
    """button action"""

    match text:
        case ' ':
            return Key.space
        case 'shift':
            return Key.shift
        case 'ctrl':
            return Key.ctrl
        case 'cmd':
            return Key.cmd
        case 'Enter':
            return Key.enter
        case _:
            return text


if __name__ == '__main__':

    _keyboard = keyboard([10, 80])
    print(_keyboard.buttons)
