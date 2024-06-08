# **Tello Drone Face Tracking - Python Script**

This Python script leverages the `djitellopy` library to control a Tello drone and `OpenCV` for face tracking in the video feed. The script is designed to track faces and control the drone accordingly. It uses multiprocessing to handle the video feed display and face tracking simultaneously.

## **Features**

- **Signal Handling**:
  - Handles keyboard interrupts and safely terminates processes.
  
- **Face Tracking**:
  - Tracks a face in the video feed and controls the Tello drone based on the position of the face.
  
- **Drone Control**:
  - Connects to the Tello drone, starts the video stream, and can take off and land.
  
- **Multiprocessing**:
  - Utilizes multiprocessing to handle the video feed display and face tracking in separate processes.

[!IMPORTANT]
**BEFORE INSTALLATION**
Install the Required Dependencies:
pip install djitellopy opencv-python imutils


