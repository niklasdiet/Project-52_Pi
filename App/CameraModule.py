from time import sleep
import picamera

def take_picture():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        sleep(2)
        camera.capture('images/image.jpg')
        camera.stop_preview()
