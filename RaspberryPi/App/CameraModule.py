from time import sleep
import picamera as picamera

def take_picture():
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(2)
    camera.capture('images/image.jpg')
    camera.close()
