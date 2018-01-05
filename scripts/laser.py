import explorerhat as eh
import time
import sys



laser = o1 = eh.output.one
m1 = eh.motor.one
m2 = eh.motor.two

speed = int(sys.argv[1]) if len(sys.argv) > 1 else 50
t = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
motor_id = int(sys.argv[3]) if len(sys.argv) > 3 else 1

motor = m1 if motor_id == 1 else m2


def main():

        laser.on()

        motor.speed(speed)
        time.sleep(t)
        motor.stop()

        time.sleep(1)




        
def step(dir=1):
        m1.speed(17*dir)
        time.sleep(0.05)
        m1.stop()




def main_old():

        rounds = 5
        steps = 15
        
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



# main_old()
main()
