#!/usr/bin/python3

import sys
import os
import time
from datetime import datetime

from picamera import PiCamera

import getpass


def mk_filename():
    return datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f") 


camera_path = '/home/pi/Pictures/frog-bot/'

camera = PiCamera()
camera.rotation = 180

time_lapse_period = 30 # 5 * 60
little_sleep = 5

def time_lapse():
    print('TIMLAPSE LIBEZNICE')
    print(mk_filename(), getpass.getuser())

    num_photos_taken = 0

    while True:
        camera.resolution = (1280, 720)
        camera.framerate = 15
        camera.start_preview()
        time.sleep(little_sleep)
        camera.capture('/home/pi/Pictures/time-lapses/libeznice/libeznice_'+mk_filename()+'.jpg')
        camera.stop_preview()

        num_photos_taken += 1
        print("num_photos_taken =", num_photos_taken)

        time.sleep(time_lapse_period - little_sleep - 1)


if __name__ == "__main__":
    time_lapse()
