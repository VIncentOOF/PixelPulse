# **Tello Drone Face Tracking - Python Script**

This Python script leverages the `djitellopy` library to control a Tello drone and `OpenCV` for face tracking in the video feed. The script is designed to track human bodies using `YOLOv4-tiny` and the face using `OpenCV's Haar cascades` and control the drone accordingly. It uses multiprocessing to handle the video feed display and face tracking simultaneously.

## **Features**

- **Signal Handling**:
  - Handles keyboard interrupts and safely terminates processes.
  
- **Face Tracking**:
  - Tracks a human face in the video feed using YOLOv4-tiny for person detection and OpenCV's Haar cascades for face detection.
  - Controls the Tello drone based on the position of the detected face.
  
- **Drone Control**:
  - Connects to the Tello drone, starts the video stream, and can take off and land.
  
- **Multiprocessing**:
  - Utilizes multiprocessing to handle the video feed display and face tracking in separate processes.

[!IMPORTANT]
**BEFORE INSTALLATION**
Install the Required Dependencies:
pip install djitellopy opencv-python imutils
Download YOLOv4-tiny Files
yolov4-tiny.weights
yolov4-tiny.cfg
coco.names
Ensure Haar Cascade File is Available:
This file should be included with OpenCV: haarcascade_frontalface_default.xml (found in OpenCV's data/haarcascades directory).
or you can intall from: https://github.com/kipr/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml


