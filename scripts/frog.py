#!/usr/bin/python3

import sys
import os
import time
from datetime import datetime

from picamera import PiCamera
import explorerhat as eh
from evdev import InputDevice, categorize, ecodes, KeyEvent

import getpass
import subprocess

# constants


def mk_filename():
    return datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f") 

print(mk_filename(), getpass.getuser())

camera_path = '/home/pi/Pictures/frog-bot/'

m1_speed = 30
m2_speed = 14

m1_dir_diff_factor = 1.5

increase_factor = 1.05


# i/o handlers

camera = PiCamera()
camera.rotation = 180

gamepad = InputDevice('/dev/input/event0')

laser = o1 = eh.output.one
m1 = eh.motor.one
m2 = eh.motor.two



def increase_speed():
    global m1_speed, m2_speed
    m1_speed = min(m1_speed * increase_factor, 100)
    m2_speed = min(m2_speed * increase_factor, 100)
    print('[+SPEED] m1_speed =', m1_speed, 'm2_speed =', m2_speed)

def decrease_speed():
    global m1_speed, m2_speed
    decrease_factor = 1 / increase_factor
    m1_speed = m1_speed * decrease_factor
    m2_speed = m2_speed * decrease_factor
    print('[-SPEED] new m1_speed =', m1_speed, 'm2_speed =', m2_speed)



def pressed_right():
    print('head RIGHT!')
    m1.speed(m1_speed)

    
def pressed_left():
    print('head LEFT!')
    speed = - min(m1_dir_diff_factor * m1_speed, 100)
    m1.speed(speed)
   

    
def pressed_up():
    print('head UP!')
    m2.speed(m2_speed)

    
def pressed_down():
    print('head DOWN!')
    m2.speed(-m2_speed)

    
def stop_x():
    print('STOP-X!')
    m1.stop()

def stop_y():
    print('STOP-Y!')
    m2.stop()
    

def pressed_X():
    print('X: taking a photo.')
    filename = camera_path + mk_filename() + '.jpg'
    camera.capture(filename)
    
    
def pressed_Y():
    print('Y pressed : start recording camera clip ...')
    filename = camera_path + 'video-' + mk_filename() + '.h264'
    camera.start_recording(filename)
    
def released_Y():
    print('Y released: stop recording!')
    camera.stop_recording()

def pressed_A():
    print('A: toggling laser')
    laser.toggle()


def pressed_B():
    print('B pressed : laser on')
    laser.on()

def released_B():
    print('B released: laser off')
    laser.off()


def pressed_LEFT_SHOULDER():
    decrease_speed()

def pressed_RIGHT_SHOULDER():
    increase_speed()
    

BTN_A  = 'BTN_THUMB'
BTN_B  = 'BTN_THUMB2'
BTN_X0 = 'BTN_JOYSTICK'
BTN_Y  = 'BTN_TOP'

BTN_START = 'BTN_BASE4'
BTN_SELECT = 'BTN_BASE3'
BTN_LEFT_SHOULDER = 'BTN_TOP2'
BTN_RIGHT_SHOULDER = 'BTN_BASE'

ABS_LOW  = 0
ABS_HIGH = 255
ABS_STOP = 127

do_restart_script = False

def main():
    global do_restart_script
    
    for event in gamepad.read_loop():
        
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            key_code = key_event.keycode
            
            if key_event.keystate == KeyEvent.key_down:
                if key_code[0]== BTN_X0: pressed_X()
                elif key_code == BTN_Y : pressed_Y()
                elif key_code == BTN_A : pressed_A()
                elif key_code == BTN_B : pressed_B()
                elif key_code == BTN_LEFT_SHOULDER : pressed_LEFT_SHOULDER()
                elif key_code == BTN_RIGHT_SHOULDER : pressed_RIGHT_SHOULDER()
                elif key_code == BTN_SELECT: break
                elif key_code == BTN_START : do_restart_script = True; break 
                else : print('Pressed key_code =', key_code)

            elif key_event.keystate == KeyEvent.key_up:
                if   key_code == BTN_B : released_B()
                elif key_code == BTN_Y : released_Y()
            
        elif event.type == ecodes.EV_ABS:
            val = event.value
            code = event.code

            if code == 0:
                if   val == ABS_LOW : pressed_left()
                elif val == ABS_HIGH: pressed_right()
                elif val == ABS_STOP: stop_x()
            elif code == 1:
                if   val == ABS_LOW : pressed_up()
                elif val == ABS_HIGH: pressed_down()
                elif val == ABS_STOP: stop_y()


def restart_script():
    #camera.close()
    #eh.explorerhat_exit() # still blinking ...
    # path = os.path.realpath(__file__)
    #argv0 = sys.argv[0]
    # os.execl(path, argv0) # problém s kamerou a právama
    # print(path)
    #print(argv0)
    #subprocess.run(argv0) # problém: pak blioká, páč je otevřeno víc explorer hatů
    print("Restart turned off, sorry!")
                
                
if __name__ == "__main__":
    print('Frog script at your service, bro!')
    main()
    if do_restart_script:
        restart_script()
