import re
from .utils import _checksum

class ReadLine:
    def __init__(self, serial_device):
        """Construct a fast serial ReadLine object with buffer.

        Parameters
        ----------
        serial_device : Serial object from pyserial
            The serial device to read from.
        """
        self.buf = b""
        self.Serial = serial_device

    def readonce(self, chunk_size=7, header=b'\t', footer=b'\n'):
        """Read the first complete chunk of data from the serial port.
        format: | header (1)| msg (n) | checksum (1) | footer (1) |
        *number in () indicates number of bytes.

        Parameters
        ----------
        chunk_size : int
            size from header to footer in bytes.
        header : bytes
            the header byte.
        footer : bytes
            the footer byte.

        Returns
        -------
        msg : bytes
            the message in the first complete chunk of data in the buffer.
            returns None if pattern not found and store bytes in buffer.
        """
        if len(header) != 1 or len(footer) != 1:
            raise ValueError("invalid length of bytes for header or footer")
        # header = int.from_bytes(header, byteorder="big")
        # footer = int.from_bytes(footer, byteorder="big")

        tmp = self.buf + self.Serial.read(chunk_size)
        pattern = rb"(%s)(.{%d})(%s)"%(header, chunk_size - 2, footer)
        m = re.match(pattern, tmp)
        if m is None:
            return None
        if _checksum(m.group(2)):
            msg = m.group(2)[:-1]
            return msg
        else:
            return None

    def readchunks(self, chunk_size=7, header=b'\t', footer=b'\n'):
        """Read all complete chunk of bytes in the buffer.

        Parameters
        ----------
        chunk_size : int
            size from header to footer in bytes.
        header : bytes
            the header byte.
        footer : bytes
            the footer byte.

        Returns
        -------
        msgs : list of bytes
            All messages from complete chunks of bytes in the buffer.
        """
        if len(header) != 1 or len(footer) != 1:
            raise ValueError("invalid length of bytes for header or footer")

        multiplier = max(1, self.Serial.in_waiting//chunk_size)
        lines = self.buf + self.Serial.read(multiplier*chunk_size)
        pattern = rb"(%s)(.{%d})(%s)"%(header, chunk_size - 2, footer)
        matches = [m for m in re.finditer(pattern, lines)]
        checked_sum = [m for m in matches if _checksum(m.group(2))]

        msgs = [m.group(2) for m in checked_sum]
        # unused end bytes are saved in buffer
        i = max([m.end() for m in checked_sum])
        self.buf = lines[i:]

        return msgs

    def readlast(self, chunk_size=7, header=b'\t', footer=b'\n'):
        """Read the last complete chunk of bytes in the buffer.
        The bytes in the buffer before the last chunk are discarded.

        Parameters
        ----------
        chunk_size : int
            size from header to footer in bytes.
        header : bytes
            the header byte.
        footer : bytes
            the footer byte.

        Returns
        -------
        msg : list of bytes
            The message from the last complete chunks of bytes in the buffer.
        """
        msg = self.readchunks(chunk_size=7, header=b'\t', footer=b'\n')
        msg = msg[-1]
        return msg


