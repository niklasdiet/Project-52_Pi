import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 960)
    camera.start_preview()
    time.sleep(2)  # Allow the camera to warm up
    camera.capture('image.jpg')
    camera.stop_preview()