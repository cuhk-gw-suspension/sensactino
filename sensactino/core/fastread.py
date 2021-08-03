

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
        [self.s.readline() for _ in range(2)]

    def readline(self):
        """Readline from the serial port.

        Returns
        -------
        r : bytearray
            All bytes until the last \\n seperator.
        """
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

    def lastline(self):
        """Return last line of byte string in the buffer.
        """
        lines = self.readline()
        last = lines.split(b"\n")[-2]
        return last


