import cv2
import mediapipe as mp
import pyautogui as pg
import autopy
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.mediapipe.python.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7)
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
ScreenSize = pg.size()


class HMRunner:
    def __init__(self, defaultState={}):
        self.state = defaultState
        self.events = []
        self.ScreenSize = ScreenSize

    def addEvent(self, func, name):
        self.events.append({
            "func": func,
            "name": name
        })

    def run(self):
        while True:
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for event in self.events:
                        if event["func"](handLms, self):
                            img = cv2.flip(img, 1)
                            cv2.putText(
                                img, event["name"], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA), 1
                            img = cv2.flip(img, 1)
                            print(event["name"])
                    mpDraw.draw_landmarks(
                        img, handLms, mpHands.HAND_CONNECTIONS)

            img = cv2.flip(img, 1)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
