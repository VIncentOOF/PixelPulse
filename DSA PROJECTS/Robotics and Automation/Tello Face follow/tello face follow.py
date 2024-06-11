import cv2
from djitellopy import Tello
import signal
import sys
import imutils
from multiprocessing import Process, Pipe, Event
import numpy as np

# Function to handle keyboard interrupt and terminate processes safely
def signal_handler(sig, frame):
    print("Signal Handler")
    if tello:
        try:
            tello.streamoff()
            tello.land()
        except:
            pass
    sys.exit()

# Load YOLO model
def load_yolo_model():
    net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return net, output_layers, classes

# Function to track a face in the video feed and control a Tello drone accordingly
def track_face_in_video_feed(exit_event, show_video_conn, fly=False, max_speed_limit=90):
    global tello
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    max_speed_threshold = max_speed_limit
    tello = Tello()
    tello.connect()
    tello.streamon()
    frame_read = tello.get_frame_read()
    
    net, output_layers, classes = load_yolo_model()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    if fly:
        tello.takeoff()
        tello.move_up(70)

    while not exit_event.is_set():
        frame = frame_read.frame
        frame = imutils.resize(frame, width=400)
        H, W, _ = frame.shape

        centerX = W // 2
        centerY = H // 2

        # YOLO object detection
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        
        person_detected = False
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and classes[class_id] == "person":  # Detect persons
                    centerX = int(detection[0] * W)
                    centerY = int(detection[1] * H)
                    w = int(detection[2] * W)
                    h = int(detection[3] * H)
                    x = centerX - w // 2
                    y = centerY - h // 2
                    person_detected = True
                    person_frame = frame[y:y + h, x:x + w]
                    break

        if person_detected:
            # Face detection within the detected person frame
            gray = cv2.cvtColor(person_frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (fx, fy, fw, fh) in faces:
                cv2.rectangle(person_frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
                fx_center = fx + fw // 2
                fy_center = fy + fh // 2
                cv2.circle(person_frame, (fx_center, fy_center), 5, (0, 0, 255), -1)
                break

        # Send the frame to the show_video function
        show_video_conn.send(frame)

# Function to display video feed
def show_video(exit_event, pipe_conn):
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        frame = pipe_conn.recv()
        cv2.imshow("Drone Face Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit_event.set()
            break

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    run_pid = True
    track_face = True
    fly = True

    # Create communication pipes between processes
    parent_conn, child_conn = Pipe()

    # Use Event for termination signal between processes
    exit_event = Event()

    # Start the show_video process
    p2 = Process(target=show_video, args=(exit_event, parent_conn,))
    p2.start()
    
    # Start the track_face_in_video_feed process
    p1 = Process(target=track_face_in_video_feed, args=(exit_event, child_conn, fly,))
    p1.start()

    # Wait for the track_face_in_video_feed process to finish
    p1.join()

    # Terminate the show_video process
    p2.terminate()
    
    # Wait for the show_video process to finish
    p2.join()

    print("Complete...")
