from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

# MediaPipe initialization
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize video capture
capture = cv2.VideoCapture(0)

def generate_frames():
    with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
        while True:
            ret, frame = capture.read()
            if not ret:
                break

            # Convert the frame to RGB for MediaPipe processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            # Reconvert the image back to BGR for OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks if available
            try:
                landmarks = results.pose_landmarks.landmark
                features = np.array([
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP].y,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP].z,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP].z,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE].z,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].z,
                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y,
                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].z,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].z
                ])
            except AttributeError:
                features = np.zeros(18)

            # Draw the pose landmarks on the image
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Encode the frame for streaming
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            # Yield frame for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
