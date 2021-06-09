import cv2
import mediapipe as mp
import time

#Video capture from the main camera
cap = cv2.VideoCapture(0)

#IMporting hands from mediapipe.solutions file for hand detection
mpHands = mp.solutions.hands
hands = mpHands.Hands()

#To draw the landmarks on the image
mpDraw = mp.solutions.drawing_utils


p_time = 0
c_time = 0

while 1:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #Getting Landmarks from result and drawint it on to the video feed
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #Getting pixel value
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 4 :
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    #FPS calculation
    c_time = time.time()
    fps = 1/(c_time-p_time)
    p_time = c_time

    #Adding FPS Text to the Video
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
