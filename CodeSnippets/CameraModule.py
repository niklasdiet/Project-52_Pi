'''import os
import cv2

def take_picture():
    # Ensure the images directory exists
    images_dir = 'images'
    os.makedirs(images_dir, exist_ok=True)

    # Create a connection to the camera
    with cv2.VideoCapture(0) as cap:
        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
        else:
            # Capture a single frame
            ret, frame = cap.read()
            
            if ret:
                # Save the captured frame as an image
                image_path = os.path.join(images_dir, 'image.jpg')
                cv2.imwrite(image_path, frame)
                print(f"Image saved at {image_path}")
            else:
                print("Error: Failed to capture frame.")

                '''