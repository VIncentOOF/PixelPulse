import cv2
import mediapipe as mp
import pickle
import os

gesture_labels = ['Up', 'Down', 'Left', 'Right', 'Forward', 'Back']

# Create a directory to save gesture data if it doesn't exist
if not os.path.exists('gesture_data'):
    os.makedirs('gesture_data')

# Assign the MediaPipe hands detection solution to mpHands and define the confidence level
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# When we detect the hand, we can use mp.solution to plot the location and connection
mpDraw = mp.solutions.drawing_utils

def capture_gesture(label):
    cap = cv2.VideoCapture(0)  # Capture video from the webcam
    print(f"Capturing gesture for {label}. Press 's' to save the gesture.")

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for handlms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, handlms, mpHands.HAND_CONNECTIONS)

        cv2.imshow('Capture Gesture', frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('s') and result.multi_hand_landmarks:
            # Save the first detected hand landmarks
            hand_landmarks = result.multi_hand_landmarks[0]
            landmark_list = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
            with open(f'gesture_data/{label}.pkl', 'wb') as f:
                pickle.dump(landmark_list, f)
            print(f"Gesture for {label} saved.")
            break
        elif key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    for label in gesture_labels:
        capture_gesture(label)


