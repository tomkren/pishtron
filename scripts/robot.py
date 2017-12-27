from time import *
import explorerhat as eh
import RPi.GPIO as GPIO

print("My robot script running!")

m1 = eh.motor.one
m2 = eh.motor.two

def stop():
	m1.forwards(0)
	m2.forwards(0)

def move_motor(motor, speed):
	if speed >= 0: motor.forwards(speed)
	else:          motor.backwards(-speed)

def mov(t, s1=100, s2=100):
	move_motor(m1,s1)
	move_motor(m2,s2)
	sleep(t)
	stop()

def forw(t,s=100):
	mov(t,s,s)

def back(t,s=100):
	mov(t,-s,-s)

def left(t,s=100):
	mov(t,s,0)

forw(0.5, 100)
sleep(1)
forw(0.5,-50)
sleep(1)
back(0.5, 50)
