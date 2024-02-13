from time import sleep
import cv2

def take_picture():
    
    # Open the camera
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera

    # Capture a single frame
    ret, frame = cap.read()

    # Save the frame to an image file
    cv2.imwrite("images/image.jpg", frame)

    # Release the camera
    cap.release()

