#!/usr/bin/python3

from evdev import InputDevice, categorize, ecodes, KeyEvent
gamepad = InputDevice('/dev/input/event0')


def pressed_left():
    print('LEFT!')

def pressed_right():
    print('RIGHT!')

def pressed_up():
    print('UP!')

def pressed_down():
    print('DOWN!')


def pressed_X():
    print('X!')

def pressed_Y():
    print('Y!')

def pressed_A():
    print('A!')

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
        else:  # Y-axis
            if val == 0:
                pressed_up()
            elif val == 255:
                pressed_down()

