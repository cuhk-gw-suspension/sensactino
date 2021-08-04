import re

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

    def readchunks(self, chunk_size=7, header=b'\t', footer=b'\n'):
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
                    if self.buf[k+chunk_size-1] == footer:
                        lines.append(self.buf[k+1:k+chunk_size-1])
            return lines


        i = self.buf.find(header)
        if i >= 0:
            r = _exhaust()
            if len(r) > 0:
                self.buf[0:] = self.buf[max(r)+1:]
                return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.buf[0:] + self.s.read(i)
            i = data.find(header)
            if i >= 0:
                r = _exhaust()
                if len(r) > 0:
                    self.buf[0:] = self.buf[max(r)+1:]
                    return r

        chunks = re.findall(rb"%s.{%d}%s" % (header, chunk_size-2, footer),
                            self.buf)
        if len(chunks) > 0:
            for i in len(self.buf):
            if self.buf[i+1-chunk_size] == header:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.buf[0:] + self.s.read(i)
            # i = data.rfind(footer)
            chunks = re.findall(rb"%s.{%d}%s" % (header, chunk_size-2, footer),
                                data)
            if len(chunks) > 0:
                h = i+1-chunk_size
                if data[:1] == header and _checksum(data[h:i]):
                    r = data[:i+1]
                    self.buf[0:] = data[i+1:]
                    return r
            else:
                self.buf.extend(data)

    def lastchunk(self):
        """Return last chunk of bytes in the buffer.
        """
        lines = self.readchunk()
        last = lines.split(b"\n")[-2]
        return last


