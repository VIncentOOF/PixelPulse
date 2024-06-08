import cv2
from djitellopy import Tello
import signal
import sys
import imutils
from multiprocessing import Process, Pipe, Event

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

    if fly:
        tello.takeoff()
        tello.move_up(70)

    while not exit_event.is_set():
        frame = frame_read.frame
        frame = imutils.resize(frame, width=400)
        H, W, _ = frame.shape

        centerX = W // 2
        centerY = H // 2

        # Display a circle at the center of the frame
        cv2.circle(frame, center=(centerX, centerY), radius=5, color=(0, 0, 255), thickness=-1)

        # Send the frame to the show_video function
        show_video_conn.send(frame)

# Function to display video feed
def show_video(exit_event, pipe_conn):
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        frame = pipe_conn.recv()
        cv2.imshow("Drone Face Tracking", frame)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit_event.set()

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
