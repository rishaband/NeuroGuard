from flask import Flask, render_template, Response
from flask_cors import CORS
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

# MediaPipe initialization
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize video capture
capture = cv2.VideoCapture(0)

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

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

            # Initialize variables
            status = "Standing"
            color = (0, 255, 0)  # Default to green

            # Extract landmarks if available
            try:
                landmarks = results.pose_landmarks.landmark

                # Extract features including x, y, z coordinates
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

                # Extract required landmarks for bounding box
                head = np.array([landmarks[mp_pose.PoseLandmark.NOSE].x, landmarks[mp_pose.PoseLandmark.NOSE].y])
                ankle_left = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y])
                ankle_right = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y])
                hip_left = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y])
                hip_right = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y])
                knee_left = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y])
                knee_right = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y])

                # Calculate bounding box
                x_min = int(min(head[0], hip_left[0], hip_right[0], ankle_left[0], ankle_right[0]) * image.shape[1])
                x_max = int(max(head[0], hip_left[0], hip_right[0], ankle_left[0], ankle_right[0]) * image.shape[1])
                y_min = int(min(head[1], hip_left[1], ankle_left[1], ankle_right[1]) * image.shape[0])
                y_max = int(max(ankle_left[1], ankle_right[1]) * image.shape[0])

                # Calculate distances for standing/falling detection
                hip_knee_diff = calculate_distance(
                    (hip_left[0], hip_left[1]), 
                    (knee_left[0], knee_left[1])
                )
                knee_ankle_diff = calculate_distance(
                    (knee_left[0], knee_left[1]),
                    (ankle_left[0], ankle_left[1])
                )

                # Define a threshold for falling detection
                fall_threshold = 0.1  # Adjust this threshold based on your needs

                if hip_knee_diff < fall_threshold and knee_ankle_diff < fall_threshold:
                    status = "Falling"
                    color = (0, 0, 255)  # Red for falling
                else:
                    status = "Standing"
                    color = (0, 255, 0)  # Green for standing

                # Draw the pose landmarks on the image
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Draw rectangle and status
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)  # Rectangle color based on status
                cv2.putText(image, status, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

            except AttributeError:
                # Default to standing if landmarks are not detected
                status = "Standing"
                color = (0, 255, 0)  # Green for standing

            # Encode the frame for streaming
            ret, buffer = cv2.imencode('.jpg', image)
            if not ret:
                continue
            
            frame = buffer.tobytes()

            # Yield frame for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return 'testing valid'

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
