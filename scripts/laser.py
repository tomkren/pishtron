import explorerhat as eh
import time

o1 = eh.output.one
m1 = eh.motor.one

def step(dir=1):
	m1.speed(16*dir)
	time.sleep(0.02)
	m1.stop()


rounds = 5
steps = 20


for round in range(rounds):

	print("{} / {}".format(round+1, rounds))

	for i in range(steps):
		o1.on()
		time.sleep(0.05)
		o1.off()
		time.sleep(0.05)

	o1.on()

	for i in range(steps):
		step()
		time.sleep(0.02)

	for i in range(steps*2):
		step(-1)
		time.sleep(0.02)

	for i in range(steps):
        	step()
        	time.sleep(0.02)

