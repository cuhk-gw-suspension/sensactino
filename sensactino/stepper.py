import serial
import time
import numpy as np

from .core.utils import _send_command

class Stepper:
    def __init__(self, port, baudrate, timeout=1):
        """Save configuration of the serial communication to the stepper.

        Parameters
        ----------
        port : str
            Path to the stepper serial control port.
        baudrate: int
            Baudrate of the serial communication.
        timeout: int, optional
            Timeout of the serial communication.
        """
        self._serial_para = {"port": port,
                             "baudrate": baudrate,
                             "timeout": timeout}

    def __enter__(self):
        """Open serial port to the stepper using parameters from __init__.
        """
        self.serial = serial.Serial(**self._serial_para)
        self.serial.flush()
        while( self.serial.out_waiting != 0):       # wait for flush to finish
            time.sleep(.001)
        line = self.serial.readline()
        print(line.decode('utf-8'))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Safely close serial port to the stepper.
        """
        self.serial.close()

    def moveto(self, position):
        """Command the stepper to move to the specified position.
        Positive direction is indicated by DIR_pin=LOW.
        Origin is the position where the stepper is initialized.

        Parameters
        ----------
        position : int
            Target position to move to, in steps.
            The stepper will try to move to this position as soon as
            the function is called.
        """
        if isinstance(position, int) or np.issubdtype(position, np.integer):
            # cmd = [b'M',
            #        position.to_bytes(4, byteorder="big", signed=True),
            #        b'\n']
            # cmd = b"".join(cmd)
            cmd = "M" + str(position) + "\n"
            _send_command(self.command, cmd)
        else:
            raise TypeError("position must be of type int.")

    def move(self, displacement):
        """Command the stepper to move displacement relative to
        the current position. Positive direction is indicated by DIR_pin=LOW.
        Origin is the position where the stepper is initialized.

        Parameters
        ----------
        displacement: int
            Relative position to move to, in steps.
            The stepper will try to move to this position as soon as
            the function is called.
        """
        if isinstance(displacement, int) or \
           np.issubdtype(displacement, np.integer):
            # cmd = [b'S',
            #        displacement.to_bytes(4, byteorder="big", signed=True),
            #        b'\n']
            # cmd = b"".join(cmd)
            cmd = "S" + str(displacement) + "\n"
            _send_command(self.serial, cmd)
        else:
            raise TypeError("displacement must be of type int.")


    # def reset(self):
    #     """Move the stepper to the center of the rail.
    #     """
    #     cmd = "R\n"
    #     cmd = cmd.encode("ascii")
    #     self.serial.write(cmd)


