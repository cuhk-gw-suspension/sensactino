from stepper.core import Stepper

with Stepper(port="/dev/ttyUSB0", baudrate=500000, timeout=10) as stepper:
    stepper.moveto(10000)

