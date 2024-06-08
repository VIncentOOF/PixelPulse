import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import pyttsx3
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()

cap = cv2.VideoCapture(0)

# Set desired resolution
wid, hei = input("enter your resolution in the format width*height (1280 720)").split()
# Set desired resolution
desired_width = int(wid)
desired_height = int(hei)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# Check if the resolution was set correctly
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f'Resolution set to: {width}x{height}')

detector = pm.poseDetector()
count = 0
direction = 0
feedback = ""
last_feedback = ""
mode = int(input("Enter 0 for 1 min time trial and 1 for training: "))

def pullup_counter():
    global count, direction, feedback, last_feedback
    ret, img = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        elbow = detector.findAngle(img, 11, 13, 15)
        shoulder = lmList[11][2]  # Y-coordinate of the left shoulder
        hip = lmList[23][2]  # Y-coordinate of the left hip

        # Bar to show Pull-up progress based on shoulder position
        bar = np.interp(shoulder, (height - 100, 100), (height - 100, 50))
        per = np.interp(shoulder, (height - 100, 100), (0, 100))

        # Check for full range of motion for the pull-up
        if per == 0:
            if shoulder <= 100:
                feedback = "Up"
                if direction == 0:
                    count += 0.5
                    direction = 1
            else:
                feedback = "Partial Up"

        if per == 100:
            if shoulder >= height - 100:
                feedback = "Down"
                if direction == 1:
                    count += 0.5
                    direction = 0
            else:
                feedback = "Partial Down"

        # Determine vocal feedback for partial reps
        if feedback == "Partial Up":
            vocal_feedback = "Pull higher."
        elif feedback == "Partial Down":
            vocal_feedback = "Lower fully."
        else:
            vocal_feedback = feedback

        # Speak the feedback if it changes
        if vocal_feedback != last_feedback:
            engine.say(vocal_feedback)
            engine.runAndWait()
            last_feedback = vocal_feedback

        print(count)

        # Draw Bar
        cv2.rectangle(img, (width - 60, 50), (width - 40, height - 100), (0, 255, 0), 3)
        cv2.rectangle(img, (width - 60, int(bar)), (width - 40, height - 100), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (width - 80, height - 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Pull-up counter
        cv2.rectangle(img, (0, height - 100), (100, height), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, height - 25), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        # Feedback
        cv2.rectangle(img, (width - 140, 0), (width, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (width - 130, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    return img

if mode == 1:
    while cap.isOpened():
        img = pullup_counter()
        cv2.imshow('Pullup counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if mode == 0:
    start_time = time.time()
    while cap.isOpened() and (time.time() - start_time) < 60:
        img = pullup_counter()
        elapsed_time = int(time.time() - start_time)
        remaining_time = 60 - elapsed_time

        # Display remaining time
        cv2.putText(img, f'Time: {remaining_time}s', (width - 250, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.imshow('Pullup counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Announce the number of pull-ups done
    engine.say(f"Time's up! You did {int(count)} pull-ups.")
    engine.runAndWait()

    cap.release()
    cv2.destroyAllWindows()
