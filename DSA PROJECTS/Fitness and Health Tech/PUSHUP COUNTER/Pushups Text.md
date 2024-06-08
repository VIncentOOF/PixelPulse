# **Pushup Counter with Form Correction - Python Script**

This Python script uses OpenCV and MediaPipe to count pushups and provide real-time feedback on form. It uses text-to-speech for vocal feedback to help users maintain proper pushup form. The script can be run in either a timed mode or a continuous training mode.

## **Features**

- **Real-time Pushup Counting**:
  - Detects and counts pushups in real-time.
  - Uses MediaPipe for pose detection and OpenCV for video processing.
  
- **Form Correction Feedback**:
  - Provides real-time feedback on pushup form.
  - Uses text-to-speech (pyttsx3) to give vocal feedback for form corrections.

- **Two Modes of Operation**:
  - **Training Mode**: Continuously counts pushups with form feedback.
  - **Timed Mode**: Runs a 1-minute time trial and counts the number of pushups completed.

[!IMPORTANT]
**BEFORE INSTALLATION**
install the libraries, you can use the following command:
pip install opencv-python mediapipe numpy pyttsx3
