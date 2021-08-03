import serial
import time
import numpy as np

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
            self._send_command(cmd)
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
            self._send_command(cmd)
        else:
            raise TypeError("displacement must be of type int.")

    def _send_command(self, cmd):
        """Handle the byte conversion and send the command to the stepper.

        Parameters
        ----------
        cmd : str-like
            command to be sent to the stepper.
        """
        if isinstance(cmd, str):
            cmd = cmd.encode("ascii")

        if not isinstance(cmd, (bytes, bytearray)):
            raise TypeError("cmd must be string-like object")
        self.serial.write(cmd)

    # def reset(self):
    #     """Move the stepper to the center of the rail.
    #     """
    #     cmd = "R\n"
    #     cmd = cmd.encode("ascii")
    #     self.serial.write(cmd)

    def sweep(self, position, fs):
        """Command the stepper to move to the positions consecutively at
        constant frequency fs.

        Parameters
        ----------
        position : int array_like
            Target position of the stepper, in steps.

        """
        dt = 1/fs
        position = np.array(position)
        timeold = time.perf_counter()
        for i in range(len(position)):
            self.moveto(position[i])

            time_not_passed = (time.perf_counter() - timeold < dt)
            while time_not_passed:
                time.sleep(1e-8)
                timenew = time.perf_counter()
                time_not_passed = (timenew - timeold < dt)
            timeold = timenew
        print("sweep finished.")

