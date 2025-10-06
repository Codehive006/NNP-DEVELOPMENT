# import os
# import cv2
# from cvzone.HandTrackingModule import HandDetector


# #varible 
# width ,height = 100,600
# folderPath= "presentation"


# #Camera setup

# cap = cv2.VideoCapture(0)
# cap.set(3,width)
# cap.set(4,height)

# # Get the list of presentation images
# pathImages = sorted(os.listdir(folderPath),key=len)
# print(pathImages)


# #variables
# imgNumber = 4
# hs,ws = int(120*1),int(212*1)
# gestureThreshold = 300

# # Hand detector
# detector = HandDetector(detectionCon=0.8,maxHands=1)




# while True:

#     # Import images 
#     success,img = cap.read()
#     img = cv2.flip(img,1)
#     pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
#     imgCurrent = cv2.imread(pathFullImage)


#     hands, img =  detector.findHands(img)
#     cv2.line(img,(0, gestureThreshold),(width,gestureThreshold),(0,255,0),10)

#     if hands:
#         hand = hands[0]
#         fingers = detector.fingersUp(hand)
#         print(fingers)

        


    
#     #Adding webcam image on the slide
#     imgSmall = cv2.resize(img,(ws,hs))
#     h,w,_ = imgCurrent.shape
#     imgCurrent[0:hs,w-ws:w] = imgSmall

#     cv2.imshow("Image",img)
#     cv2.imshow("Slides",imgCurrent)

#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break

import os
import cv2
from cvzone.HandTrackingModule import HandDetector

# --- Variables ---
width, height = 1280, 720  # Camera resolution
folderPath = "presentation"

# --- Camera setup ---
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# --- Get all presentation images ---
pathImages = sorted(os.listdir(folderPath), key=len)
print("Loaded Slides:", pathImages)

# --- Parameters ---
imgNumber = 0
gestureThreshold = 300  # Green divider line
detector = HandDetector(detectionCon=0.8, maxHands=1)

# --- Webcam overlay size (percentage of main image) ---
overlay_scale = 0.25  # 25% of slide width

while True:
    success, img = cap.read()
    if not success:
        print("Error: Camera not accessible.")
        break

    img = cv2.flip(img, 1)

    # Load current slide
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    if imgCurrent is None:
        print(f"Error: Image {pathFullImage} not found.")
        break

    # Resize slide to match webcam resolution for consistent display
    imgCurrent = cv2.resize(imgCurrent, (width, height))

    # Hand detection
    hands, img = detector.findHands(img)

    # Draw gesture threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 3)

    # Finger detection print
    # if hands:
    #     hand = hands[0]
    #     fingers = detector.fingersUp(hand)
    #     cx,cy = hand['center']
    #     print(f"Fingers: {fingers}")
        
    #     if cy < gestureThreshold: #if hand is at the height of the face

    #         # Gesture 1 - left
    #         if fingers == [1,0,0,0,0]:
    #             print("left")

    if hands:
      hand = hands[0]
    vfingers = detector.fingersUp(hand)
    cx, cy = hand['center']
    print(f"Fingers: {fingers} | Center Y: {cy}")

    # Draw a circle at hand center for debugging
    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

    # Check if hand is above gesture threshold line
    if cy < gestureThreshold:
        # Gesture 1 – Left (Thumb up only)
        if fingers == [1, 0, 0, 0, 0]:
            print("Gesture: LEFT")
            imgNumber = max(0, imgNumber - 1)  # move to previous slide
            cv2.putText(imgCurrent, "LEFT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

        # Gesture 2 – Right (Index finger up only)
        elif fingers == [0, 1, 0, 0, 0]:
            print("Gesture: RIGHT")
            imgNumber = min(imgNumber + 1, len(pathImages) - 1)  # move to next slide
            cv2.putText(imgCurrent, "RIGHT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)

        # Optional: Pause / Select (Two fingers up)
        elif fingers == [0, 1, 1, 0, 0]:
            print("Gesture: SELECT / PAUSE")
            cv2.putText(imgCurrent, "PAUSE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)




    # --- Add webcam overlay on slide (top-right corner) ---
    # Calculate new webcam overlay size
    ws = int(width * overlay_scale)
    hs = int((ws / img.shape[1]) * img.shape[0])
    imgSmall = cv2.resize(img, (ws, hs))

    # Place webcam image safely in top-right corner
    h_slide, w_slide, _ = imgCurrent.shape
    x_offset = w_slide - ws - 20  # 20px margin from right
    y_offset = 20  # margin from top

    imgCurrent[y_offset:y_offset + hs, x_offset:x_offset + ws] = imgSmall

    # --- Show results ---
    cv2.imshow("Webcam Feed", img)
    cv2.imshow("Presentation Slide", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
