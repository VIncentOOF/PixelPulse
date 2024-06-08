import cv2
import mediapipe as mp
import pickle
import os

gesture_labels = ['Up', 'Down', 'Left', 'Right', 'Forward', 'Back']

# Assign the MediaPipe hands detection solution to mpHands and define the confidence level
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# When we detect the hand, we can use mp.solution to plot the location and connection
mpDraw = mp.solutions.drawing_utils

# Function to load gesture data
def load_gesture_data():
    gesture_data = {}
    for label in gesture_labels:
        with open(f'gesture_data/{label}.pkl', 'rb') as f:
            gesture_data[label] = pickle.load(f)
    return gesture_data

# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2) ** 0.5

# Function to recognize gesture
def recognize_gesture(hand_landmarks, gesture_data):
    min_distance = float('inf')
    recognized_gesture = 'Unknown'
    
    for label, saved_landmarks in gesture_data.items():
        distance = sum(calculate_distance(hand_landmarks[i], saved_landmarks[i]) for i in range(21))
        if distance < min_distance:
            min_distance = distance
            recognized_gesture = label

    return recognized_gesture

def hand_detection():
    gesture_data = load_gesture_data()
    cap = cv2.VideoCapture(0)  # Capture video from the webcam

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        gesture = 'Unknown'  # Initialize gesture variable
        
        if result.multi_hand_landmarks:
            for handlms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, handlms, mpHands.HAND_CONNECTIONS)
                
                # Convert landmarks to a list of tuples
                hand_landmarks = [(lm.x, lm.y, lm.z) for lm in handlms.landmark]
                gesture = recognize_gesture(hand_landmarks, gesture_data)
                break

        cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    hand_detection()
