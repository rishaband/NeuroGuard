#Imports used
import mediapipe as mp
import numpy as np
import cv2 as cv
from datetime import datetime
import time
import os

# Define the global variable for tracking last execution time
last_execution_time = 0
delay = 30  # Delay in seconds
filename = "fall.txt"

def create_and_write_to_file(filename):
    try:
        # Get the current date and time
        now = datetime.now()
        
        # Format the date and time
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Print the current directory and filename for debugging
        print(f"Writing to file: {filename}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Create or open the file in append mode ('a' will create the file if it doesn't exist)
        with open(filename, 'a') as file:
            file.write(f"{formatted_datetime}\n")
        print(f"Data successfully written to {filename}")
    
    except IOError as e:
        print(f"IOError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


mp_drawing = mp.solutions.drawing_utils  # Drawing utility for visualizing poses
mp_pose = mp.solutions.pose  # Pose estimation model

# Define fall detection thresholds
FALL_THRESHOLD_HIP_ANKLE_Y = 0.2  # Adjusted threshold for fall detection (more lenient)
FALL_THRESHOLD_HEAD_ANKLE_Y = 0.5  # Threshold for head-to-ankle Y-axis difference for standing detection

# Video Feed (Live Footage)
capture = cv.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            print("Frames could not be captured properly") # error catching for frames
            break

        # Convert the frame to RGB colours
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # Temporarily make the image non-writeable for performance
        image.flags.writeable = False

        # Process the image with MediaPipe Pose
        results = pose.process(image)

        # Reconvert the image back to RGB for OpenCV
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        # Extract landmarks if they exist (nodes)
        try:
            landmarks = results.pose_landmarks.landmark

            # Extract 3D coordinates for key points (head, hips, knees, ankles) => used from mediapose to detect falls
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

            # Extract individual points for hips, ankles, and head
            left_hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_HIP].y])
            right_hip = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y])
            left_ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y])
            right_ankle = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y])
            head = np.array([landmarks[mp_pose.PoseLandmark.NOSE].x,
                             landmarks[mp_pose.PoseLandmark.NOSE].y])

            # Average positions for hips, ankles, and head
            avg_hip_y = (left_hip[1] + right_hip[1]) / 2
            avg_ankle_y = (left_ankle[1] + right_ankle[1]) / 2
            avg_head_y = head[1]

            # Calculate vertical difference (head-to-ankle and hip-to-ankle)
            hip_ankle_y_diff = avg_ankle_y - avg_hip_y  # Reversed logic here
            head_ankle_y_diff = avg_ankle_y - avg_head_y  # Reversed logic here

            # Standing Logic
            if hip_ankle_y_diff > FALL_THRESHOLD_HIP_ANKLE_Y and head_ankle_y_diff > FALL_THRESHOLD_HEAD_ANKLE_Y:
                status_text = "Standing"
                color = (0, 225, 0)  # Green for standing

            else: # Falling Logic
                status_text = "Falling"
                color = (0, 0, 225)  # Red for falling
                #print("Fall detected! Features:", features)  # Print features only when falling
                
                current_time = time.time()
                if current_time - last_execution_time >= delay:
                    # Call the function if 30 seconds have passed
                    create_and_write_to_file("fall.txt")

                    last_execution_time = current_time  # Update last execution time

            # Draw a rectangle around the body using head, hips, and ankles
            x_min = int(min(left_hip[0], right_hip[0], left_ankle[0], right_ankle[0], head[0]) * frame.shape[1])
            x_max = int(max(left_hip[0], right_hip[0], left_ankle[0], right_ankle[0], head[0]) * frame.shape[1])
            y_min = int(min(left_hip[1], right_hip[1], left_ankle[1], right_ankle[1], head[1]) * frame.shape[0])
            y_max = int(max(left_hip[1], right_hip[1], left_ankle[1], right_ankle[1], head[1]) * frame.shape[0])

            # Draw the rectangle on the frame
            cv.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)

            # Display the status text
            cv.putText(image, status_text, (x_min, y_min - 10), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv.LINE_AA)

        except AttributeError:
            features = np.zeros(18)  # Handle the case where landmarks are not detected => cases where person is too close/far from camera
            print("No landmarks detected")

        # Draw pose landmarks on the image
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display the frame with landmarks and rectangle
        cv.imshow('Feed', image)

        # Break the loop on 'q' key press (live stream ends)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    

    capture.release()
    cv.destroyAllWindows()