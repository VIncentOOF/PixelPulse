import cv2
import mediapipe as mp
import threading
import logging
import time
from djitellopy import Tello

# Assign tello to the Tello class and set the information to error only
tello = Tello()
tello.LOGGER.setLevel(logging.ERROR)  # Ignore INFO from Tello
fly = False  # For debugging purpose

# Assign the MediaPipe hands detection solution to mpHands and define the confidence level
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# When we detect the hand, we can use mp.solution to plot the location and connection
mpDraw = mp.solutions.drawing_utils


def hand_detection(tello):
    while True:
        global gesture

        # Read the frame from Tello
        frame = tello.get_frame_read().frame
        frame = cv2.flip(frame, 1)

        # Call hands from MediaPipe Solution for the hand detection, need to ensure the frame is RGB
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Read frame width & height instead of using fixed number 960 & 720
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]
        my_hand = []

        if result.multi_hand_landmarks:
            for handlms, handside in zip(result.multi_hand_landmarks, result.multi_handedness):
                if handside.classification[0].label == 'Right':  # We will skip the right hand information
                    continue

                # With mp.solutions.drawing_utils, plot the landmark location and connect them with define style
                mpDraw.draw_landmarks(frame, handlms, mpHands.HAND_CONNECTIONS,
                                      mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                                      mp.solutions.drawing_styles.get_default_hand_connections_style())

                # Convert all the hand information from a ratio into actual position according to the frame size.
                for i, landmark in enumerate(handlms.landmark):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    my_hand.append((x, y))

                # Setup left hand control with the pre-defined logic.
                finger_on = []
                if my_hand[4][0] > my_hand[2][0]:  # Thumb
                    finger_on.append(1)
                else:
                    finger_on.append(0)
                for i in range(1, 5):
                    if my_hand[4 + i * 4][1] < my_hand[2 + i * 4][1]:  # Other fingers
                        finger_on.append(1)
                    else:
                        finger_on.append(0)

                gesture = 'Unknown'
                if sum(finger_on) == 0:
                    gesture = 'Stop'
                elif sum(finger_on) == 5:
                    gesture = 'Land'
                elif sum(finger_on) == 1:
                    if finger_on[0] == 1:
                        if my_hand[8][0] < my_hand[6][0]:  # Index pointing left
                            gesture = 'Right'
                        else:  # Index pointing right
                            gesture = 'Left'
                    elif finger_on[1] == 1:
                        gesture = 'Up'
                elif sum(finger_on) == 2:
                    if finger_on[1] == 1 and finger_on[0] == 1:
                        gesture = 'Down'
                    elif finger_on[1] == 1 and finger_on[2] == 1:
                        gesture = 'Come'
                elif sum(finger_on) == 3 and finger_on[1] == finger_on[2] == finger_on[3] == 1:
                    gesture = 'Away'

        cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('Tello Video Stream', frame)
        cv2.waitKey(1)
        if gesture == 'Landed':
            break


########################
# Start of the program #
########################

# Connect to the drone via WIFI
tello.connect()

# Instruct Tello to start video stream and ensure first frame read
tello.streamon()

while True:
    frame = tello.get_frame_read().frame
    if frame is not None:
        break

# Start the hand detection thread when the drone is flying
gesture = 'Unknown'
video_thread = threading.Thread(target=hand_detection, args=(tello,), daemon=True)
video_thread.start()

# Take off the drone
time.sleep(1)
if fly:
    tello.takeoff()
    tello.set_speed(10)
    tello.move_up(80)

while True:
    hV = dV = vV = rV = 0
    if gesture == 'Land':
        break
    elif gesture == 'Stop' or gesture == 'Unknown':
        hV = dV = vV = rV = 0
    elif gesture == 'Right':
        hV = -15
    elif gesture == 'Left':
        hV = 15
    elif gesture == 'Up':
        vV = 20
    elif gesture == 'Down':
        vV = -20
    elif gesture == 'Come':
        dV = 15
    elif gesture == 'Away':
        dV = -15

    tello.send_rc_control(hV, dV, vV, rV)

# Landing the drone
if fly:
    tello.land()
gesture = 'Landed'

# Stop the video stream
tello.streamoff()

# Show the battery level before ending the program
print("Battery :", tello.get_battery())
