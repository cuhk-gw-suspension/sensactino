import serial
import time
from .core.utils import _addsum, _int2bytes, _send_command

class Actuator:
    def __init__(self, port, baudrate, timeout=5):
        """Save configuration of the serial communication for the Actuator.

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
        self.Serial = serial.Serial(**self._serial_para)
        self.Serial.flush()
        while( self.Serial.out_waiting != 0):  # wait for flush to finish
            time.sleep(.1)
        print(self.Serial.readline().decode())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Safely close serial port to the stepper.
        """
        self.Serial.close()

    def output(self, value):
        """set the output amplitude.

        Parameters
        ----------
        value : int
            value to send to the Actuator.
        """
        if isinstance(value, int) or np.issubdtype(value, np.integer):
            # value = _int2bytes(value)
            # checksum = _addsum(value)
            value = str(value)
            cmd = "S" + value + "\n"
            cmd = cmd.encode("ascii")
            _send_command(self.Serial, cmd)
        else:
            raise TypeError("position must be of type int.")

    def info(self):
        """Request the arduino to serial print information about the actuator.

        Returns
        -------
        str
            information about the actuator.
        """
        cmd = "I\n"
        cmd = cmd.encode("ascii")
        _send_command(self.Serial, cmd)
        msg = self.Serial.readline()
        msg = msg.decode()
        print(msg)
        return msg



