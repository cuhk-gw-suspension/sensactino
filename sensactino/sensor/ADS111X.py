from .base import Sensor
from ..core import I2C


class ADS111X(I2C, Sensor):
    """Class for ADS111X sensor."""
    def __init__(self, addr, sda=None, scl=None):
        I2C.__init__(self, addr, sda=sda, scl=scl)
        Sensor.__init__(self)

        self._configuration = None

    def __str__(self):
        description = {
            "class":[cls.__name__ for cls in self.__class__.mro()[:-1]],
            "configuration": self._configuration,
        }
        return str(description)

    def measure(self):
        val = self.readwrite(self._register_bytes("Conversion"), length=2)
        val = int.from_bytes(val, byteorder="big", signed=True)
        val *= self._configuration["gain"]/32767.0 #since signed 16 bits sensor
        return val

    def configure(self,
        gain=4.096,
        ain_config=0,
        mode="continuous",
        rate=250,
        window_comparator=False,
        polarity="low",
        latching=False,
        queue=None):
        """Configure ADS111X Sensor using specified read write method.

        Parameters
        ----------
        gain : float
            Gain amplifier configuration.
            Gain from [6.144, 4.096, 2.048, 1.024, 0.512, 0.256] can be used.
            A ValueError would be raised if other values was used.
        ain_config : int
            input multiplexer configuration for ads1115.
            ain_config range from 0 to 7, corresponding to the respective bits
            for input selection.
        mode : str, optional
            Set the operation mode of ADS1115.
            mode from ['single', 'continuous'] can be selected.
        rate : int, optional
            SPS of ads1115.
            rate from [8, 16, 32, 64, 128, 250, 475, 860] can be selected.
            Default to 128SPS.
        window_comparator : bool, optional
            True to use Window Comparator. False to use Traditional comparator.
            Default to False.
        polarity : str, optional
            "high" or "low". Controls the polarity of the ALERT/RDY pin.
        latching : bool, optional
            Toggle latching ALERT/RDY pin. Default to False.
        queue : int or None
            Set the number of successive conversion before asserting
            the ALERT/RDY pin.
            None disables the comparator.
        """
        kwargs = locals()
        kwargs.pop("self", None)
        send = self._config_bytes(**kwargs)
        self.readwrite(send, length=0)

    def _register_bytes(self, register):
        """return the register bytes of ads1115.

        Parameters
        ----------
        register : str
            "Conversion", "Config", "Lo_thresh", or "Hi_thresh".
        """
        REGISTER_ADDR = {"Conversion": 0x00,
                          "Config": 0x01,
                          "Lo_thresh": 0x02,
                          "Hi_thresh": 0x03}
        return REGISTER_ADDR[register]

    def _config_bytes(
        self,
        gain=4.096,
        ain_config=0,
        mode="continuous",
        rate=128,
        window_comparator=False,
        polarity="low",
        latching=False,
        queue=None):
        """Config bytes for ADS111X Sensor.

        Parameters
        ----------
        gain : float
            Gain amplifier configuration.
            Gain from [6.144, 4.096, 2.048, 1.024, 0.512, 0.256] can be used.
            A ValueError would be raised if other values was used.
        ain_config : int
            input multiplexer configuration for ads1115.
            ain_config range from 0 to 7, corresponding to the respective bits
            for input selection.
        mode : str, optional
            Set the operation mode of ADS1115.
            mode from ['single', 'continuous'] can be selected.
        rate : int, optional
            SPS of ads1115.
            rate from [8, 16, 32, 64, 128, 250, 475, 860] can be selected.
            Default to 128SPS.
        window_comparator : bool, optional
            True to use Window Comparator. False to use Traditional comparator.
            Default to False.
        polarity : str, optional
            "high" or "low". Controls the polarity of the ALERT/RDY pin.
        latching : bool, optional
            Toggle latching ALERT/RDY pin. Default to False.
        queue : int or None
            Set the number of successive conversion before asserting
            the ALERT/RDY pin.
            None disables the comparator.

        Returns
        -------
        List of bytes
            The required bytes for ads1115 configuration(excluding address).
        """
        for option in [window_comparator, latching]:
            if not isinstance(option, bool):
                raise TypeError("type must be of boolean")

        CONFIG_OPTIONS = {
            "ain_config": range(8),
            "gain": (6.144, 4.096, 2.048, 1.024, 0.512, 0.256),
            "mode": ("continuous", "single"),
            "rate": (8, 16, 32, 64, 128, 250, 475, 860),
            "window_comparator": (False, True),
            "polarity": ("low", "high"),
            "latching": (False, True),
            "queue": (1, 2, 4, None)}

        firstbyte = CONFIG_OPTIONS["mode"].index(mode)
        firstbyte <<= 3
        firstbyte += CONFIG_OPTIONS["ain_config"].index(ain_config)
        firstbyte <<= 3
        firstbyte += CONFIG_OPTIONS["gain"].index(gain)
        firstbyte <<= 1
        firstbyte += CONFIG_OPTIONS["mode"].index(mode)

        secondbyte = CONFIG_OPTIONS["rate"].index(rate)
        secondbyte <<= 1
        secondbyte += window_comparator
        secondbyte <<= 1
        secondbyte += CONFIG_OPTIONS["polarity"].index(polarity)
        secondbyte <<= 1
        secondbyte += latching
        secondbyte <<= 2
        secondbyte += CONFIG_OPTIONS["queue"].index(queue)

        self._configuration = locals()
        sent_bytes = [self._register_bytes("Config"), firstbyte, secondbyte]
        return sent_bytes


