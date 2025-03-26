import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
    max_num_hands=1
)

mp_draw = mp.solutions.drawing_utils

def get_distance(a, b):
    """Calculate the Euclidean distance between two points."""
    return np.linalg.norm(np.array(a) - np.array(b))

def get_finger_tips(landmarks):
    """Get the coordinates of the index finger tip, middle finger tip, and thumb tip."""
    index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    return (index_tip.x, index_tip.y), (middle_tip.x, middle_tip.y), (thumb_tip.x, thumb_tip.y), (ring_tip.x, ring_tip.y), (pinky_tip.x, pinky_tip.y)

def detect_gestures(landmarks):
    """Detect gestures like scroll up, scroll down, screenshot, move cursor, and click."""
    if landmarks:
        index_finger, middle_finger, thumb, ring_finger, pinky = get_finger_tips(landmarks)

        all_fingers_up = (
            index_finger[1] < thumb[1] and
            middle_finger[1] < thumb[1] and
            ring_finger[1] < thumb[1] and
            pinky[1] < thumb[1]
        )

        index_middle_up = (
            index_finger[1] < thumb[1] and
            middle_finger[1] < thumb[1]
        )

        index_up = (
            index_finger[1] < thumb[1] and
            middle_finger[1] > thumb[1] and
            ring_finger[1] > thumb[1] and
            pinky[1] > thumb[1]
        )

        index_down = (
            index_finger[1] > thumb[1] and
            middle_finger[1] > thumb[1] and
            ring_finger[1] > thumb[1] and
            pinky[1] > thumb[1]
        )

        thumb_up = (
            thumb[1] < index_finger[1] and
            thumb[1] < middle_finger[1] and
            thumb[1] < ring_finger[1] and
            thumb[1] < pinky[1]
        )

        pinky_up = (
            pinky[1] < index_finger[1] and
            pinky[1] < middle_finger[1] and
            pinky[1] < ring_finger[1] and
            pinky[1] < thumb[1]
        )

        if all_fingers_up:
            return 'move_cursor'
        elif index_middle_up:
            return 'screenshot'
        elif index_up:
            return 'scroll_up'
        elif index_down:
            return 'scroll_down'
        elif pinky_up:
            return 'click'
    
    return None

def process_gesture(frame, landmark_list, hand_landmarks):
    """Process gestures and perform actions like scrolling, screenshot, moving the cursor, or clicking."""
    gesture = detect_gestures(hand_landmarks)

    if gesture == 'screenshot':
        screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')
        pyautogui.screenshot(screenshot_path)
        cv2.putText(frame, "Screenshot Taken", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        print(f"Screenshot saved at {screenshot_path}")
    
    elif gesture == 'scroll_up':
        pyautogui.scroll(80)
        cv2.putText(frame, "Scrolling Up", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    elif gesture == 'scroll_down':
        pyautogui.scroll(-80)
        cv2.putText(frame, "Scrolling Down", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    elif gesture == 'move_cursor':
        index_finger, _, _, _, _ = get_finger_tips(hand_landmarks)
        screen_width, screen_height = pyautogui.size()
        cursor_x = int(index_finger[0] * screen_width)
        cursor_y = int(index_finger[1] * screen_height)
        pyautogui.moveTo(cursor_x, cursor_y)
        cv2.putText(frame, "Moving Cursor", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    elif gesture == 'click':
        pyautogui.click()
        cv2.putText(frame, "Click Detected", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def hand_gesture_control():
    """Main function to capture video and process hand gestures."""
    cap = cv2.VideoCapture(0)
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frame_rgb)
            
            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))
                process_gesture(frame, landmark_list, hand_landmarks)
            
            cv2.imshow('Hand Gesture Control', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    hand_gesture_control()