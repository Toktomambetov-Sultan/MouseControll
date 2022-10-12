import cv2
import mediapipe as mp
import time
import pyautogui as pg
pg.FAILSAFE = False
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.mediapipe.python.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7)
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
ScreenSize = pg.size()
while True:
	success, img = cap.read()
	imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	results = hands.process(imgRGB)
	if results.multi_hand_landmarks:
		for handLms in results.multi_hand_landmarks:
			for id,lm in enumerate(handLms.landmark):
				if id==0:
					x = (lm.x - 0.4)/0.2
					if lm.x<=0.4:
						x = 0	
					elif lm.x>=0.6:
						x = 1	
					y = (lm.y - 0.4)/0.2
					if lm.x<=0.4:
						x = 0	
					elif lm.x>=0.6:
						x = 1
					pg.moveTo(ScreenSize.width*(1-x),ScreenSize.height*y,duration=0.05)
			mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
	cv2.imshow("Image",img)
	cv2.waitKey(1)
