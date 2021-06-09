#Hand Tracking Module File
import cv2
import mediapipe as mp
import time

class handDetector:
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Importing hands from mediapipe.solutions file for hand detection
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)

        # To draw the landmarks on the image
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # Getting Landmarks from result and draw it on to the video feed
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []

        if self.results.multi_hand_landmarks:
            self.myhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(self.myhand.landmark):
                # Getting pixel value
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy]);
                if draw:
                    if id == 4:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList

def main():
    p_time = 0
    c_time = 0
    detector = handDetector()
    # Video capture from the main camera
    cap = cv2.VideoCapture(0)
    while 1:
        success, img = cap.read()

        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        # FPS calculation
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        # Adding FPS Text to the Video
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()