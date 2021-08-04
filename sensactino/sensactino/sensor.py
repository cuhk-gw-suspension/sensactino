import serial
from .core.fastread import ReadLine
from .core.utils import _checksum

class Sensor:
    def __init__(self, port, baudrate, timeout=1):
        """Save configuration of the serial communication from the sensor.

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
        self.FastRead = ReadLine(self.Serial)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Safely close serial port to the stepper.
        """
        self.Serial.close()

    def talk(self):
        """Send a character to arduino so that arduino output a measurement.

        Returns
        -------
        value : int
        """
        self.Serial.write(b"o")
        tmp =bytearray(8)
        tmp[0:] = self.Serial.read(8)
        while tmp[:1] != header:
            tmp <<= 1
            tmp[-1:] = self.Serial.read()



    def measure(self, if_error="use last value"):
        """Return the digital value of the last measurement from the sensor.

        Parameters
        ----------
        if_error : str
            The instruction when checksum is not correct.
            Choose from "l", "r", "use last value", "read again".
            "l", "use last value": using the last measurement.
            "r", "read again": measure recusively until checksum matches

        Returns
        -------
        value : int
        """
        expr = ["l", "r", "use last value", "read again"]
        checklist = [if_error is word for word in expr]
        if not any(checklist):
            raise ValueError("argument for if_error does not match any"
                             + "instruction")
        line = self.FastRead.lastline()
        line = line.rstrip()

        if _checksum(line):
            self._value = int.from_bytes(line[:-1],
                                         byteorder="big",
                                         signed=True)
            return self._value
        else:
            if if_error == 'r' or if_error == 'read again':
                self.measure(if_error='r')
            elif if_error == 'l' or if_error == 'use last value':
                return self._value

    def read(self):
        """Return the lines of bytes received from the sensor until last b'\\n'.
        Used for debugging.

        Return
        -------
        line : bytes
             All bytes until the last b'\\n'.
        """
        return self.FastRead.readline()




