import cv2
import mediapipe as mp
import time
import pyautogui as pg
import autopy
import asyncio
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.mediapipe.python.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7)
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
ScreenSize = pg.size()
is_clicked = False
async def sleep(): 
	global is_clicked
	await asyncio.sleep(0.5)
	is_clicked = False
	
	
while True:
	success, img = cap.read()
	imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	results = hands.process(imgRGB)
	if results.multi_hand_landmarks:
		for handLms in results.multi_hand_landmarks:
			for id,lm in enumerate(handLms.landmark):
				if id==0:
					try:
						x = (lm.x - 0.2)/0.6	
						if x>=1: x = 1
						if x<=0: x = 0
						y = (lm.y - 0.3)/0.4	
						if y>=1: y = 1
						if y<=0: y = 0
						autopy.mouse.move(ScreenSize.width*(1-x),ScreenSize.height*y)
					except Exception as inst: 
						print("Error: ", inst)
			if handLms.landmark[4] != None and handLms.landmark[8] != None and not is_clicked : 
				x1,y1,z1 = handLms.landmark[4].x,handLms.landmark[4].y,handLms.landmark[4].z
				x2,y2,z2 = handLms.landmark[8].x,handLms.landmark[8].y,handLms.landmark[8].z
				lenght = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
				if lenght <= 0.005:
					is_clicked = True
					autopy.mouse.click()
					asyncio.run(sleep())
			mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
	cv2.imshow("Image",cv2.flip(img,1))
	cv2.waitKey(1)

# import handMatching 
# a = handMatching()

# def detect(landmarks): ...
# a.apply(detect)
# a.run()