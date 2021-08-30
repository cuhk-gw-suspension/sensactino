from abc import abstractmethod


class I2C:
    def __init__(self, addr, sda=None, scl=None):
        """Constructor for Sensor using I2C protocol.

        Parameters
        ----------
        addr : int or bytes
            I2C address of the sensor.
        sda : int, optional
            sda pin number on the master device.
        scl : int, optional
            scl pin number on the master device.
        """
        self.addr = addr
        self.sda = sda
        self.scl = scl
        self.i2c = None

    def readwrite(self, send, length=0, **kwargs):
        """function to read or/and write data through I2C protocol.

        Parameters
        ----------
        send : list of bytes(int)
            bytes to send to the slave device, excluding address.
        length : int, optional
            Number of bytes to read.
            Default to 0.

        Returns
        -------
        bytes
            bytes read, if any.
        """
        if self.master == "labjack":
            if isinstance(send, (bytes, bytearray)):
                send = list(send)
            if isinstance(send, int):
                send = [send]
            res = self.i2c(self.addr,
                           send,
                           SDAPinNum=self.sda,
                           SCLPinNum=self.scl,
                           NumI2CBytesToReceive=length,
                           **kwargs)
            return res["I2CBytes"]
        elif self.master == "custom":
            res_bytes = self.i2c(self.addr, send, length, **kwargs)
            return res_bytes

    def use_custom_method(self, fun):
        """Use custom method to read or/and write data through i2c protocol.

        Parameters
        ----------
        fun : callable
            The function to use for sending and reading bytes through i2c.
            fun(addr, send_bytes, num_bytes2read, **kwargs) -> bytes from i2c.
        """
        self.i2c = fun

    def use_labjack(self, device):
        """Use labjack device to connect to the sensor.

        Parameters
        ----------
        device : labjack device object
            The device to connect to.
        """
        from LabJackPython import Device

        if issubclass(type(device), Device):
            self.master = "labjack"
            self.i2c = device.i2c
        else:
            raise TypeError("device must be of LabJackPython Device subclass.")

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value):
        if isinstance(value, bytes):
            value = list(value)
            if len(value) == 1:
                value = value[0]
            else:
                raise ValueError("Invalid i2c address:", bytes(value))

        if isinstance(value, int):
            if value < 0 or value > 0x7F:
                raise ValueError("Invalid i2c address:", hex(value))
            self._addr = value
        else:
            raise TypeError("addr must be of type int.")

    @property
    def sda(self):
        return self._sda

    @sda.setter
    def sda(self, sda):
        if isinstance(sda, (int, type(None))):
            self._sda = sda
        else:
            raise TypeError("Invalid type of sda:", type(sda),
                            "\nsda must be of type int or NoneType")

    @property
    def scl(self):
        return self._scl

    @scl.setter
    def scl(self, scl):
        if isinstance(scl, (int, type(None))):
            self._scl = scl
        else:
            raise TypeError("Invalid type of scl:", type(scl),
                            "\nscl must be of type int or NoneType")

    @property
    def i2c(self):
        return self._i2c

    @i2c.setter
    def i2c(self, fun):
        if callable(fun):
            self._i2c = fun
        elif fun is not None:
            raise TypeError("readwrite must be callable")
