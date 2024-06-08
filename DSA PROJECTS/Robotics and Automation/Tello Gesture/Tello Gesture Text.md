# **Tello Drone Gesture Control - Python Script**

This Python script utilizes the `djitellopy` library to control a Tello drone and `MediaPipe` for hand gesture recognition. The script is designed to detect hand gestures and control the drone accordingly. It also includes scripts to capture and recognize hand gestures for training purposes.

## **Features**

- **Signal Handling**:
  - Handles termination signals and safely terminates processes.
  
- **Hand Gesture Detection**:
  - Uses MediaPipe to detect hand gestures in the video feed.
  - Recognizes specific gestures and controls the Tello drone based on the detected gestures.
  
- **Drone Control**:
  - Connects to the Tello drone, starts the video stream, and can take off and land.
  - Executes drone movements based on recognized hand gestures.
  
- **Gesture Capture and Recognition**:
  - Captures hand gestures and saves them for training.
  - Recognizes pre-trained hand gestures for drone control.

[!IMPORTANT]
**BEFORE INSTALLATION**
Install the Required Dependencies:
pip install djitellopy opencv-python mediapipe

**Usage**
Run capture_gesture.py first to log in the commands
Then run tello gesture.py
