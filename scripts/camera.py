from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.start_recording('/home/pi/Desktop/video01.h264')

sleep(5)

camera.capture('/home/pi/Desktop/image01.jpg')

sleep(15)

camera.capture('/home/pi/Desktop/image02.jpg')

camera.stop_recording()
camera.stop_preview()
