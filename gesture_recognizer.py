import cv2
import mediapipe as mp
import time
import math

class GestureRecognizer:
    def __init__(self, mode=False, max_hands=1, detection_confidence=0.7, tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands,
                                         min_detection_confidence=self.detection_confidence,
                                         min_tracking_confidence=self.tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return self.lmList

    def fingers_up(self):
        fingers = []
        if not self.lmList:
            return fingers

        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def detect_gesture(self, img, prev_hand_pos, current_time, prev_time):
        current_gesture = "No Gesture"
        if not self.lmList:
            return current_gesture, prev_hand_pos, current_time

        fingers = self.fingers_up()

        x1, y1 = self.lmList[self.tipIds[1]][1], self.lmList[self.tipIds[1]][2]

        if fingers == [1, 0, 0, 0, 0]:
            current_gesture = "Thumbs Up"

        elif fingers == [1, 1, 1, 1, 1]:
            current_gesture = "Open Palm"

        elif fingers == [0, 1, 0, 0, 0]:
            current_gesture = "Index Point"

        if prev_hand_pos and self.lmList:
            prev_x, prev_y = prev_hand_pos
            current_x, current_y = self.lmList[self.tipIds[1]][1], self.lmList[self.tipIds[1]][2]

            dx = current_x - prev_x
            dy = current_y - prev_y
            dt = current_time - prev_time

            swipe_threshold_x = 50
            swipe_threshold_y = 30
            swipe_time_threshold = 0.5

            if dt > 0 and dt < swipe_time_threshold:
                if dx > swipe_threshold_x and abs(dy) < swipe_threshold_y:
                    current_gesture = "Swipe Right"
                elif dx < -swipe_threshold_x and abs(dy) < swipe_threshold_y:
                    current_gesture = "Swipe Left"

        if self.lmList:
            prev_hand_pos = (x1, y1)
            prev_time = current_time

        return current_gesture, prev_hand_pos, prev_time