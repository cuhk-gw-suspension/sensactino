from serial import Serial
import time

from .base import Sensor
from sensactino.core import ReadLine, _checksum

class ArduinoSensor(Sensor):
    def __init__(self, port, baudrate, timeout=1):
        """Save configuration of the serial communication from the sensor.

        Parameters
        ----------
        port : str
            Path to the sensor serial port.
        baudrate: int
            Baudrate of the serial communication.
        timeout: int, optional
            Timeout of the serial communication.
        """
        super().__init__()
        self._serial_para = {"port": port,
                             "baudrate": baudrate,
                             "timeout": timeout}
        self._value = 0

    def __enter__(self):
        """Open serial port to the sensor using parameters from __init__.
        """
        self.Serial = Serial(**self._serial_para)
        time.sleep(.1)
        self.Serial.flush()
        while( self.Serial.in_waiting != 0):       # wait for flush to finish
            time.sleep(.001)
        self.FastRead = ReadLine(self.Serial)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Safely close serial port to the sensor.
        """
        self.Serial.close()

    def info(self):
        """Read info about the sensor."""
        self.Serial.write(b"i")
        info = self.Serial.readline()
        print(info)
        return info

    def measure(self, if_error="l"):
        """Send a character to arduino so that arduino output a measurement.

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
        self.Serial.write(b"r")
        msg = self.FastRead.readonce(debug=self.debug)

        if msg is None:
            if if_error == "l" or if_error == "use last value":
                value = self._value
            if if_error == "r" or if_error == "read again":
                self._measure(if_error=if_error)
        else:
            value = int.from_bytes(msg, byteorder="little", signed=True)
            self._value = value
        return value


    # def measure_last(self):
    #     """Returns

        # Parameters
        # ----------
        # if_error : str
        #     The instruction when checksum is not correct.
        #     Choose from "l", "r", "use last value", "read again".
        #     "l", "use last value": using the last measurement.
        #     "r", "read again": measure recusively until checksum matches

    #     Returns
    #     -------
    #     value : int
    #     """
    #     line = self.FastRead.readlast(chunk_size=7,
    #                                   header=b'\t',
    #                                   footer=b'\n')
    #     value = int.from_bytes(line, byteorder="big", signed=True)
    #     return value

    def read_all(self):
        """Read all bytes from the sensor.
        Use for debugging.
        Caution: This method reads byte regardless of whether the transmission
        of data is in progress.

        Return
        -------
        line : bytes
             All bytes in the buffer.
        """
        n = self.Serial.in_waiting
        line = self.Serial.read(n)
        return line


