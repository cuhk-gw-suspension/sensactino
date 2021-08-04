import serial
# from .core.fastread import ReadLine
from .core.utils import _addsum, _int2bytes

class Actuator:
    def __init__(self, port, baudrate, timeout=1):
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
        while( self.Serial.out_waiting != 0):       # wait for flush to finish
            time.sleep(.001)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Safely close serial port to the stepper.
        """
        self.Serial.close()

    def out(self, value):
        """.

        Parameters
        ----------
        value : int
            value to send to the Actuator.
        """
        if isinstance(position, int) or np.issubdtype(position, np.integer):
            value = _int2bytes(value)
            checksum = _addsum(value)
            cmd = b"".join([value, checksum, b'\n'])
            _send_command(self.Serial, cmd)
        else:
            raise TypeError("position must be of type int.")


