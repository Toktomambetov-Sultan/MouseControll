import cv2
import mediapipe as mp
import time
import pyautogui as pg
import autopy
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
					try:
						autopy.mouse.move(ScreenSize.width*(1-lm.x),ScreenSize.height*lm.y)
					except Exception as inst: 
						print("Error: ", inst)
			mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
	cv2.imshow("Image",cv2.flip(img,1))
	cv2.waitKey(1)

# import handMatching 
# a = handMatching()

# def detect(landmarks): ...
# a.apply(detect)
# a.run()