import cv2 as cv
import numpy as np 

capture = cv.VideoCapture(0)

while True: 
    ret, frame = capture.read()
    if not ret: 
        print("Frames could not be captured properly")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break


capture.release() #lets go of the camera for other possible applications that require it. Ex. OBS
cv.destroyAllWindows()


#adding some more comments here to make a commit 