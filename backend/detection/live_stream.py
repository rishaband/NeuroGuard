import mediapipe as mp 
import numpy as np 
import cv2 as cv
import pandas 
mp_drawing = mp.solutions.drawing_utils # drawing utility for visualising poses 
mp_pose = mp.solutions.pose # pose estimation model -> one of the few models from media pipe 



#Video Feed 
capture = cv.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            print("Frames could not be captured properly")
            break

        # Convert the frame to RGB
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # Temporarily make the image non-writeable for performance
        image.flags.writeable = False

        # Process the image with MediaPipe Pose
        results = pose.process(image)

        # Reconvert the image back to BGR for OpenCV
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        # Extract landmarks if they exist
        try:
            landmarks = results.pose_landmarks.landmark
            # Extract coordinates for key points below the waist
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
            features = np.zeros(18)  # Handle the case where landmarks are not detected

        # Draw pose landmarks on the image
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display the frame with landmarks
        cv.imshow('Feed', image)

        # Break the loop on 'q' key press
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


    capture.release()
    cv.destroyAllWindows()






    




