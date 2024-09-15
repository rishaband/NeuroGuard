# from flask import Flask, render_template, Response
# from flask_cors import CORS  # Import CORS
# import cv2 as cv
# import mediapipe as mp
# import numpy as np
# from datetime import datetime
# import time
# import os

# # Define the global variable for tracking last execution time
# last_execution_time = 0
# delay = 30  # Delay in seconds
# filename = "fall.txt"

# def create_and_write_to_file(filename):
#     try:
#         # Get the current date and time
#         now = datetime.now()
        
#         # Format the date and time
#         formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        
#         # Print the current directory and filename for debugging
#         print(f"Writing to file: {filename}")
#         print(f"Current working directory: {os.getcwd()}")
        
#         # Create or open the file in append mode ('a' will create the file if it doesn't exist)
#         with open(filename, 'a') as file:
#             file.write(f"{formatted_datetime}\n")
#         print(f"Data successfully written to {filename}")
    
#     except IOError as e:
#         print(f"IOError occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# app = Flask(__name__)
# CORS(app)  # Initialize CORS

# mp_drawing = mp.solutions.drawing_utils  # Drawing utility for visualizing poses
# mp_pose = mp.solutions.pose  # Pose estimation model

# # Define fall detection thresholds
# FALL_THRESHOLD_HIP_ANKLE_Y = 0.2  # Adjusted threshold for fall detection (more lenient)
# FALL_THRESHOLD_HEAD_ANKLE_Y = 0.5  # Threshold for head-to-ankle Y-axis difference for standing detection

# # Video Feed (Live Footage)
# capture = cv.VideoCapture(0)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/test')
# def test():
#     return 'testing valid'

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def generate_frames():
#     with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
#         while capture.isOpened():
#             ret, frame = capture.read()
#             if not ret:
#                 print("Frames could not be captured properly") # error catching for frames
#                 break

#             # Convert the frame to RGB colours
#             image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

#             # Temporarily make the image non-writeable for performance
#             image.flags.writeable = False

#             # Process the image with MediaPipe Pose
#             results = pose.process(image)

#             # Reconvert the image back to RGB for OpenCV
#             image.flags.writeable = True
#             image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

#             # Extract landmarks if they exist (nodes)
#             try:
#                 landmarks = results.pose_landmarks.landmark

#                 # Extract 3D coordinates for key points (head, hips, knees, ankles) => used from mediapose to detect falls
#                 features = np.array([
#                     landmarks[mp_pose.PoseLandmark.LEFT_HIP].x,
#                     landmarks[mp_pose.PoseLandmark.LEFT_HIP].y,
#                     landmarks[mp_pose.PoseLandmark.LEFT_HIP].z,
#                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x,
#                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y,
#                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP].z,
#                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x,
#                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y,
#                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE].z,
#                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x,
#                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y,
#                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].z,
#                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x,
#                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y,
#                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].z,
#                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x,
#                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y,
#                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].z
#                 ])

#                 # Extract individual points for hips, ankles, and head
#                 left_hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP].x,
#                                      landmarks[mp_pose.PoseLandmark.LEFT_HIP].y])
#                 right_hip = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x,
#                                       landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y])
#                 left_ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x,
#                                        landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y])
#                 right_ankle = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x,
#                                         landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y])
#                 head = np.array([landmarks[mp_pose.PoseLandmark.NOSE].x,
#                                  landmarks[mp_pose.PoseLandmark.NOSE].y])

#                 # Average positions for hips, ankles, and head
#                 avg_hip_y = (left_hip[1] + right_hip[1]) / 2
#                 avg_ankle_y = (left_ankle[1] + right_ankle[1]) / 2
#                 avg_head_y = head[1]

#                 # Calculate vertical difference (head-to-ankle and hip-to-ankle)
#                 hip_ankle_y_diff = avg_ankle_y - avg_hip_y  # Reversed logic here
#                 head_ankle_y_diff = avg_ankle_y - avg_head_y  # Reversed logic here

#                 # Standing Logic
#                 if hip_ankle_y_diff > FALL_THRESHOLD_HIP_ANKLE_Y and head_ankle_y_diff > FALL_THRESHOLD_HEAD_ANKLE_Y:
#                     status_text = "Standing"
#                     color = (0, 225, 0)  # Green for standing

#                 else: # Falling Logic
#                     status_text = "Falling"
#                     color = (0, 0, 225)  # Red for falling
#                     #print("Fall detected! Features:", features)  # Print features only when falling
                    
#                     current_time = time.time()
#                     if current_time - last_execution_time >= delay:
#                         # Call the function if 30 seconds have passed
#                         create_and_write_to_file("fall.txt")

#                         last_execution_time = current_time  # Update last execution time

#                 # Draw a rectangle around the body using head, hips, and ankles
#                 x_min = int(min(left_hip[0], right_hip[0], left_ankle[0], right_ankle[0], head[0]) * frame.shape[1])
#                 x_max = int(max(left_hip[0], right_hip[0], left_ankle[0], right_ankle[0], head[0]) * frame.shape[1])
#                 y_min = int(min(left_hip[1], right_hip[1], left_ankle[1], right_ankle[1], head[1]) * frame.shape[0])
#                 y_max = int(max(left_hip[1], right_hip[1], left_ankle[1], right_ankle[1], head[1]) * frame.shape[0])

#                 # Draw the rectangle on the frame
#                 cv.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)

#                 # Display the status text
#                 cv.putText(image, status_text, (x_min, y_min - 10), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv.LINE_AA)

#             except AttributeError:
#                 features = np.zeros(18)  # Handle the case where landmarks are not detected => cases where person is too close/far from camera
#                 print("No landmarks detected")

#             # Draw pose landmarks on the image
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#             # Display the frame with landmarks and rectangle
#             cv.imshow('Feed', image)

#             # Break the loop on 'q' key press (live stream ends)
#             if cv.waitKey(1) & 0xFF == ord('q'):
#                 break

#             # Encode the frame to JPEG
#             ret, buffer = cv.imencode('.jpg', image)
#             if not ret:
#                 continue
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     capture.release()
#     cv.destroyAllWindows()
# if __name__ == "__main__":
#     app.run(debug=True)
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

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
