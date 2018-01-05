import explorerhat as eh
import time
import sys



laser = o1 = eh.output.one
m1 = eh.motor.one

speed = int(sys.argv[1]) if len(sys.argv) > 1 else 50
t = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25

rounds = 5
steps = 15

def main2():

	laser.on()

	m1.speed(speed)
	time.sleep(t)
	m1.stop()



def step(dir=1):
	m1.speed(17*dir)
	time.sleep(0.05)
	m1.stop()


def main1():
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



# main1()
main2()
