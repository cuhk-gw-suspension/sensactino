from sensactino import Actuator
import time

if __name__ == '__main__':
    with Actuator("/dev/ttyUSB0", 500000, timeout=5) as my_actuator:
        # set the output level of the actuator = -1000
        # see arduino_scipt directory for arduino side script
        my_actuator.output(-1000)

