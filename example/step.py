from stepper.core import Stepper

# this demonstrate python side of using the stepper.
with Stepper(port="/dev/ttyUSB0", baudrate=500000, timeout=10) as stepper:
    stepper.moveto(10000)

