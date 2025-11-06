# import cv2
# import mediapipe as mp
# import pyautogui
# import numpy as np
# import time

# class GestureController:
#     def __init__(self):
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             static_image_mode=False,
#             max_num_hands=1,
#             min_detection_confidence=0.7,
#             min_tracking_confidence=0.7
#         )
#         self.mp_draw = mp.solutions.drawing_utils
        
#         # Improved gesture thresholds
#         self.swipe_threshold = 80
#         self.pinch_threshold = 40
#         self.thumb_index_threshold = 50
        
#         # State tracking
#         self.prev_landmarks = None
#         self.last_gesture_time = 0
#         self.gesture_cooldown = 1.0  # seconds
#         self.current_gesture = "none"
        
#         # Drawing state
#         self.is_drawing = False
#         self.last_draw_point = None
        
#     def detect_gestures(self, frame):
#         """
#         Detect hand gestures from webcam frame
#         Returns: gesture_type, annotated_frame, hand_landmarks
#         """
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = self.hands.process(rgb_frame)
        
#         gesture = "none"
#         annotated_frame = frame.copy()
#         hand_landmarks = None
        
#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 # Draw hand landmarks
#                 self.mp_draw.draw_landmarks(
#                     annotated_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
#                     self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
#                     self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2)
#                 )
                
#                 # Get landmark coordinates
#                 landmarks = []
#                 for lm in hand_landmarks.landmark:
#                     h, w, c = frame.shape
#                     landmarks.append((int(lm.x * w), int(lm.y * h)))
                
#                 # Detect gestures with cooldown
#                 current_time = time.time()
#                 if current_time - self.last_gesture_time > self.gesture_cooldown:
#                     new_gesture = self._analyze_gesture(landmarks)
#                     if new_gesture != "none" and new_gesture != self.current_gesture:
#                         gesture = new_gesture
#                         self.current_gesture = new_gesture
#                         self.last_gesture_time = current_time
                
#                 # Update previous landmarks
#                 self.prev_landmarks = landmarks
        
#         return gesture, annotated_frame, hand_landmarks
    
#     def _analyze_gesture(self, landmarks):
#         """Analyze hand landmarks to detect specific gestures"""
#         if not landmarks:
#             return "none"
        
#         # Get key points
#         thumb_tip = landmarks[4]
#         index_tip = landmarks[8]
#         middle_tip = landmarks[12]
#         ring_tip = landmarks[16]
#         pinky_tip = landmarks[20]
#         wrist = landmarks[0]
        
#         # Calculate distances
#         thumb_index_dist = self._calculate_distance(thumb_tip, index_tip)
        
#         # Improved swipe detection
#         swipe_detected = self._detect_swipe(landmarks)
#         if swipe_detected:
#             return swipe_detected
        
#         # Improved pinch detection
#         if thumb_index_dist < self.pinch_threshold:
#             # Check if other fingers are closed
#             if self._are_fingers_closed([middle_tip, ring_tip, pinky_tip], landmarks):
#                 return "pinch"
        
#         # Improved open palm detection
#         if self._is_open_palm(landmarks):
#             return "open_palm"
        
#         # Improved thumbs up detection
#         if self._is_thumbs_up(landmarks):
#             return "thumbs_up"
        
#         # Victory gesture (for drawing toggle)
#         if self._is_victory_gesture(landmarks):
#             return "victory"
        
#         # Fist gesture (for stopping drawing)
#         if self._is_fist(landmarks):
#             return "fist"
        
#         return "none"
    
#     def _detect_swipe(self, landmarks):
#         """Improved swipe detection with horizontal and vertical support"""
#         if self.prev_landmarks is None:
#             return "none"
        
#         # Use index finger tip for swipe detection
#         current_index = landmarks[8]
#         prev_index = self.prev_landmarks[8]
        
#         dx = current_index[0] - prev_index[0]
#         dy = current_index[1] - prev_index[1]
        
#         # Check for significant movement
#         if abs(dx) > self.swipe_threshold and abs(dx) > abs(dy):
#             if dx > 0:
#                 return "swipe_right"
#             else:
#                 return "swipe_left"
#         elif abs(dy) > self.swipe_threshold and abs(dy) > abs(dx):
#             if dy > 0:
#                 return "swipe_down"
#             else:
#                 return "swipe_up"
        
#         return "none"
    
#     def _is_open_palm(self, landmarks):
#         """Check if hand is in open palm position"""
#         fingertips = [8, 12, 16, 20]  # index, middle, ring, pinky
#         mcp_joints = [5, 9, 13, 17]   # knuckles
        
#         open_fingers = 0
#         for tip, mcp in zip(fingertips, mcp_joints):
#             if landmarks[tip][1] < landmarks[mcp][1]:  # If fingertip is above MCP
#                 open_fingers += 1
        
#         return open_fingers >= 3  # At least 3 fingers open
    
#     def _is_thumbs_up(self, landmarks):
#         """Improved thumbs up detection"""
#         thumb_tip = landmarks[4]
#         thumb_ip = landmarks[3]
#         index_tip = landmarks[8]
#         index_mcp = landmarks[5]
        
#         # Thumb should be extended upward and to the side
#         thumb_extended = (thumb_tip[1] < thumb_ip[1] and 
#                          thumb_tip[0] > thumb_ip[0])
        
#         # Other fingers should be closed
#         other_fingers_closed = True
#         for tip_idx in [8, 12, 16, 20]:  # All fingertips
#             mcp_idx = tip_idx - 3  # Corresponding MCP
#             if landmarks[tip_idx][1] < landmarks[mcp_idx][1]:  # If finger is open
#                 other_fingers_closed = False
#                 break
        
#         return thumb_extended and other_fingers_closed
    
#     def _is_victory_gesture(self, landmarks):
#         """Victory gesture (index and middle finger up, others down)"""
#         index_tip = landmarks[8]
#         middle_tip = landmarks[12]
#         ring_tip = landmarks[16]
#         pinky_tip = landmarks[20]
#         thumb_tip = landmarks[4]
        
#         # Check index and middle fingers are up
#         index_up = index_tip[1] < landmarks[6][1]  # Below PIP joint
#         middle_up = middle_tip[1] < landmarks[10][1]
        
#         # Check ring and pinky fingers are down
#         ring_down = ring_tip[1] > landmarks[14][1]
#         pinky_down = pinky_tip[1] > landmarks[18][1]
        
#         # Check thumb is not extended upward
#         thumb_down = thumb_tip[1] > landmarks[3][1]
        
#         return index_up and middle_up and ring_down and pinky_down and thumb_down
    
#     def _is_fist(self, landmarks):
#         """Check if hand is making a fist"""
#         fingertips = [8, 12, 16, 20]
#         mcp_joints = [5, 9, 13, 17]
        
#         closed_fingers = 0
#         for tip, mcp in zip(fingertips, mcp_joints):
#             if landmarks[tip][1] > landmarks[mcp][1]:  # If fingertip is below MCP
#                 closed_fingers += 1
        
#         return closed_fingers >= 3  # At least 3 fingers closed
    
#     def _are_fingers_closed(self, finger_tips, landmarks):
#         """Check if specific fingers are closed"""
#         for tip in finger_tips:
#             # Simple check - if fingertip is below wrist level
#             if tip[1] < landmarks[0][1]:  # If above wrist
#                 return False
#         return True
    
#     def _calculate_distance(self, point1, point2):
#         """Calculate Euclidean distance between two points"""
#         return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
#     def get_index_finger_position(self, landmarks, frame_shape):
#         """Get normalized index finger position for drawing"""
#         if not landmarks or not landmarks.landmark:
#             return None
        
#         index_tip = landmarks.landmark[8]
#         h, w = frame_shape[:2]
        
#         # Convert to screen coordinates (normalized 0-1)
#         x = index_tip.x
#         y = index_tip.y
        
#         return (x, y)

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
from collections import deque

class GestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Gesture state
        self.current_gesture = "none"
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.5  # seconds between gestures
        
        # Movement tracking
        self.movement_history = deque(maxlen=10)
        self.prev_index_pos = None
        
        # Gesture thresholds (tuned for better detection)
        self.swipe_threshold_x = 100  # pixels
        self.swipe_threshold_y = 80   # pixels
        self.pinch_threshold = 35     # pixels
        self.stationary_threshold = 15 # pixels
        
        # Finger state thresholds
        self.finger_extended_threshold = 0.8
        self.finger_closed_threshold = 0.3
        
        print("Gesture Controller Initialized with Improved Algorithms")

    def detect_gestures(self, frame):
        """
        Main gesture detection function with improved algorithms
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gesture = "none"
        annotated_frame = frame.copy()
        hand_landmarks = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks with better visibility
                self.mp_draw.draw_landmarks(
                    annotated_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=3, circle_radius=4),
                    self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=3)
                )
                
                # Get all landmarks
                landmarks = []
                h, w, c = frame.shape
                for lm in hand_landmarks.landmark:
                    landmarks.append((int(lm.x * w), int(lm.y * h)))
                
                # Detect gestures with improved algorithms
                current_time = time.time()
                if current_time - self.last_gesture_time > self.gesture_cooldown:
                    new_gesture = self._analyze_hand_gesture(landmarks, hand_landmarks.landmark)
                    if new_gesture != "none" and new_gesture != self.current_gesture:
                        gesture = new_gesture
                        self.current_gesture = new_gesture
                        self.last_gesture_time = current_time
                        print(f"Gesture Detected: {gesture}")
                
                # Update movement history for swipe detection
                self._update_movement_history(landmarks[8] if landmarks else None)  # Index finger tip
                
                # Add gesture text to frame
                cv2.putText(annotated_frame, f"Gesture: {gesture}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        return gesture, annotated_frame, hand_landmarks

    def _analyze_hand_gesture(self, landmarks, normalized_landmarks):
        """
        Improved gesture analysis using multiple detection methods
        """
        if not landmarks or len(landmarks) < 21:
            return "none"
        
        # Method 1: Count extended fingers
        extended_fingers = self._count_extended_fingers(normalized_landmarks)
        
        # Method 2: Check specific gesture patterns
        gesture = self._check_gesture_patterns(landmarks, normalized_landmarks, extended_fingers)
        
        # Method 3: Detect swipes from movement history
        if gesture == "none":
            swipe_gesture = self._detect_swipe_from_history()
            if swipe_gesture != "none":
                gesture = swipe_gesture
        
        return gesture

    def _count_extended_fingers(self, landmarks):
        """
        Count how many fingers are extended using improved logic
        """
        finger_states = {
            'thumb': False,
            'index': False,
            'middle': False,
            'ring': False,
            'pinky': False
        }
        
        # Finger tip landmarks
        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [3, 6, 10, 14, 18]  # PIP joints
        finger_mcps = [2, 5, 9, 13, 17]   # MCP joints
        
        for i, (tip, pip, mcp) in enumerate(zip(finger_tips, finger_pips, finger_mcps)):
            # For thumb, use different logic
            if i == 0:  # Thumb
                # Check if thumb is extended to the side
                thumb_tip = landmarks[tip]
                thumb_ip = landmarks[pip]
                thumb_mcp = landmarks[mcp]
                
                # Calculate angles or distances for thumb
                thumb_extended = (thumb_tip.x < thumb_ip.x and 
                                abs(thumb_tip.y - thumb_ip.y) < 0.1)
                finger_states['thumb'] = thumb_extended
            else:
                # For other fingers: tip should be above PIP joint
                finger_extended = landmarks[tip].y < landmarks[pip].y
                finger_name = ['index', 'middle', 'ring', 'pinky'][i-1]
                finger_states[finger_name] = finger_extended
        
        return finger_states

    def _check_gesture_patterns(self, landmarks, normalized_landmarks, finger_states):
        """
        Check for specific gesture patterns
        """
        # Open Palm (all fingers extended)
        if (finger_states['index'] and finger_states['middle'] and 
            finger_states['ring'] and finger_states['pinky']):
            return "open_palm"
        
        # Victory Gesture (index and middle extended, others closed)
        if (finger_states['index'] and finger_states['middle'] and 
            not finger_states['ring'] and not finger_states['pinky'] and 
            not finger_states['thumb']):
            return "victory"
        
        # Thumbs Up (only thumb extended)
        if (finger_states['thumb'] and not finger_states['index'] and 
            not finger_states['middle'] and not finger_states['ring'] and 
            not finger_states['pinky']):
            return "thumbs_up"
        
        # Fist (all fingers closed)
        if (not finger_states['thumb'] and not finger_states['index'] and 
            not finger_states['middle'] and not finger_states['ring'] and 
            not finger_states['pinky']):
            return "fist"
        
        # Pinch (thumb and index close together)
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        thumb_index_dist = np.sqrt((thumb_tip[0]-index_tip[0])**2 + (thumb_tip[1]-index_tip[1])**2)
        
        if thumb_index_dist < self.pinch_threshold:
            # Make sure other fingers are somewhat closed
            middle_tip = landmarks[12]
            ring_tip = landmarks[16]
            pinky_tip = landmarks[20]
            
            wrist = landmarks[0]
            hand_size = np.sqrt((wrist[0]-landmarks[9][0])**2 + (wrist[1]-landmarks[9][1])**2)
            
            # Check if other fingers are above their MCP joints (closed)
            if (middle_tip[1] > landmarks[10][1] and 
                ring_tip[1] > landmarks[14][1] and 
                pinky_tip[1] > landmarks[18][1]):
                return "pinch"
        
        return "none"

    def _update_movement_history(self, current_index_pos):
        """
        Track finger movement for swipe detection
        """
        if current_index_pos is None:
            return
        
        current_time = time.time()
        self.movement_history.append((current_time, current_index_pos))
        
        # Keep only recent history
        while self.movement_history and current_time - self.movement_history[0][0] > 2.0:
            self.movement_history.popleft()

    def _detect_swipe_from_history(self):
        """
        Detect swipe gestures from movement history
        """
        if len(self.movement_history) < 3:
            return "none"
        
        # Get the oldest and newest positions
        old_time, old_pos = self.movement_history[0]
        new_time, new_pos = self.movement_history[-1]
        
        # Calculate movement
        dx = new_pos[0] - old_pos[0]
        dy = new_pos[1] - old_pos[1]
        dt = new_time - old_time
        
        # Only detect if movement is fast enough
        if dt < 0.5:  # Swipe should be quick
            # Horizontal swipe
            if abs(dx) > self.swipe_threshold_x and abs(dx) > abs(dy) * 1.5:
                if dx > 0:
                    return "swipe_right"
                else:
                    return "swipe_left"
            
            # Vertical swipe
            elif abs(dy) > self.swipe_threshold_y and abs(dy) > abs(dx) * 1.5:
                if dy > 0:
                    return "swipe_down"
                else:
                    return "swipe_up"
        
        return "none"

    def get_index_finger_position(self, landmarks, frame_shape):
        """Get normalized index finger position for drawing"""
        if not landmarks or not landmarks.landmark:
            return None
        
        index_tip = landmarks.landmark[8]
        h, w = frame_shape[:2]
        
        # Convert to screen coordinates (normalized 0-1)
        x = index_tip.x
        y = index_tip.y
        
        return (x, y)

    def reset_gesture_state(self):
        """Reset gesture state"""
        self.current_gesture = "none"
        self.movement_history.clear()
        self.prev_index_pos = None