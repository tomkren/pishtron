#!/usr/bin/python3

import explorerhat as eh
import time
import sys

laser = o1 = eh.output.one
m1 = eh.motor.one
m2 = eh.motor.two


from evdev import InputDevice, categorize, ecodes, KeyEvent
gamepad = InputDevice('/dev/input/event0')


m1_speed = 30
# m1_step_time = 0.015

m2_speed = 14
# m2_step_time = 0.01

def pressed_left():
    print('LEFT!')
    m1.speed(-m1_speed*1.5)
    # time.sleep(m1_step_time)
    # m1.stop()

    
def pressed_right():
    print('RIGHT!')
    m1.speed(m1_speed)
    # time.sleep(m1_step_time)
    # m1.stop()

def stop_x():
    print('STOP-X!')
    m1.stop()

def stop_y():
    print('STOP-Y!')
    m2.stop()
    
def pressed_up():
    print('UP!')
    m2.speed(m2_speed)
    # time.sleep(m2_step_time)
    # m2.stop()

    
def pressed_down():
    print('DOWN!')
    m2.speed(-m2_speed)
    # time.sleep(m2_step_time)
    # m2.stop()

def pressed_X():
    print('X!')

def pressed_Y():
    print('Y!')

def pressed_A():
    print('A: toggling laser')
    laser.toggle()


def pressed_B():
    print('B!')

    
for event in gamepad.read_loop():
    # print(event)
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        # print(keyevent)
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.keycode[0] == 'BTN_JOYSTICK':
                pressed_X()
            elif keyevent.keycode == 'BTN_THUMB':
                pressed_A()
            elif keyevent.keycode == 'BTN_THUMB2':
                pressed_B()
            elif keyevent.keycode == 'BTN_TOP':
                pressed_Y()
    elif event.type == ecodes.EV_ABS:
        val = event.value
        if event.code == 0:  # X-axis
            if val == 0:
                pressed_left()
            elif val == 255:
                pressed_right()
            elif val == 127:
                stop_x()
        else:  # Y-axis
            if val == 0:
                pressed_up()
            elif val == 255:
                pressed_down()
            elif val == 127:
                stop_y()

