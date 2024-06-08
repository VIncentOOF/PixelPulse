import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import pyttsx3
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()

cap = cv2.VideoCapture(0)
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
form = 0
feedback = "Fix Form"
last_feedback = ""
mode = int(input("Enter 0 for 1 min time trial and 1 for training: "))

def pushup_counter():
    global count, direction, form, feedback, last_feedback
    ret, img = cap.read() 
    width = int(cap.get(3))  
    height = int(cap.get(4))  

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        elbow = detector.findAngle(img, 11, 13, 15)
        shoulder = detector.findAngle(img, 13, 11, 23)
        hip = detector.findAngle(img, 11, 23, 25)
        
        # Percentage of success of pushup
        per = np.interp(elbow, (90, 160), (0, 100))
        
        # Bar to show Pushup progress
        bar = np.interp(elbow, (90, 160), (height - 100, 50))

        # Check to ensure right form before starting the program
        if elbow > 160 and shoulder > 40 and hip > 160:
            form = 1

        # Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if elbow <= 90 and hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                    
            if per == 100:
                if elbow > 160 and shoulder > 40 and hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                        # form = 0

        # Determine vocal feedback for form correction
        if feedback == "Fix Form":
            if elbow <= 90:
                vocal_feedback = "Lower your elbows."
            elif shoulder <= 40:
                vocal_feedback = "Raise your shoulders."
            elif hip <= 160:
                vocal_feedback = "Raise your hips."
            else:
                vocal_feedback = "Fix your form."
        else:
            vocal_feedback = feedback

        # Speak the feedback if it changes
        if vocal_feedback != last_feedback:
            engine.say(vocal_feedback)
            engine.runAndWait()
            last_feedback = vocal_feedback

        print(count)
        
        # Draw Bar
        if form == 1:
            cv2.rectangle(img, (width - 60, 50), (width - 40, height - 100), (0, 255, 0), 3)
            cv2.rectangle(img, (width - 60, int(bar)), (width - 40, height - 100), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (width - 80, height - 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Pushup counter
        cv2.rectangle(img, (0, height - 100), (100, height), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, height - 25), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
        
        # Feedback 
        cv2.rectangle(img, (width - 140, 0), (width, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (width - 130, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    return img

if mode == 1:
    while cap.isOpened():
        img = pushup_counter()
        cv2.imshow('Pushup counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if mode == 0:
    start_time = time.time()
    while cap.isOpened() and (time.time() - start_time) < 60:
        img = pushup_counter()
        elapsed_time = int(time.time() - start_time)
        remaining_time = 60 - elapsed_time

        # Display remaining time
        cv2.putText(img, f'Time: {remaining_time}s', (width - 250, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.imshow('Pushup counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Announce the number of pushups done
    engine.say(f"Time's up! You did {int(count)} push-ups.")
    engine.runAndWait()

    cap.release()
    cv2.destroyAllWindows()
