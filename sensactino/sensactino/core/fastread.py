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
        self.buf = bytearray()
        self.s = serial_device

        # discard possible null bytes from initialization
        [self.s.read() for _ in range(2)]
    
    def readbytes(self, chunk_size=7, header=b'\t', footer=b'\n'):
        """Read chunks of data from the serial port.
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
        r : bytearray
            All bytes until the last chunk.
        """

        def _exhaust():
            tmp = [k for k in range(len(self.buf)) if self.buf[k:k+1] == header]
            lines = []
            for k in tmp:
                if k+chunk_size < len(self.buf):
                    f = self.buf[k+chunk_size-1:k+chunk_size]
                    s = self.buf[k+1:k+chunk_size-1]
                    msg = s[:-1]
                    if f == footer and _checksum(s):
                            lines.append(msg)
            return max(tmp), lines


        i = self.buf.find(header)
        if i >= 0:
            index, r = _exhaust()
            if len(r) > 0:
                self.buf[0:] = self.buf[max(index)+1:]
                return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.buf[0:] + self.s.read(i)
            i = data.find(header)
            if i >= 0:
                index, r = _exhaust()
                if len(r) > 0:
                    self.buf[0:] = self.buf[max(index)+1:]
                    return r
            elif len(self.buf) >= 255:
                self.extend(data)

        # chunks = re.findall(rb"%s.{%d}%s" % (header, chunk_size-2, footer),
        #                     self.buf)

    def lastchunk(self):
        """Return last chunk of bytes in the buffer.
        """
        lines = self.readchunk()
        last = lines.split(b"\n")[-2]
        return last


