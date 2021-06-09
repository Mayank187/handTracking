#Adjusting System Volume
import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

#Using pyautogui for increasing and decreasing volume of the system
import pyautogui

p_time = 0
c_time = 0
detector = htm.handDetector()

# Video capture from the main camera
cap = cv2.VideoCapture(0)

p_thumb = 0
c_thumb = 0
while 1:
    success, img = cap.read()

    img = detector.findHands(img,draw=False)

    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        p_thumb = p_thumb if p_thumb != 0 else lmList[4][1]
        c_thumb = lmList[4][1]
        #Using pervious thumb postion and current thumb position to reduce or increace volume
        if p_thumb>c_thumb and p_thumb-c_thumb > 10:
            pyautogui.press('volumeup')
            p_thumb = c_thumb
        elif p_thumb<c_thumb and c_thumb-p_thumb > 10:
            pyautogui.press('volumedown')
            p_thumb = c_thumb

    # FPS calculation
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    # Adding FPS Text to the Video
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
