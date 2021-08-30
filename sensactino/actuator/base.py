from abc import abstractmethod


class Actuator:
    """Base class for all actuators.

	Attributes
    ----------
    reading : int, float or array
        The reading of sensor.
    """
    def __init__(self):
        """Constructor

		Parameters
        ----------
        label : str or None, optional
            Label for this sensor.
            Defaults to None
        """
        self.debug = False

    @abstractmethod
    def output(self):
        """Method to adjust actuator's output."""
        pass

    @abstractmethod
    def configure(self):
        """Method to configure the actuator, if available."""
        pass

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, boolean):
        if isinstance(boolean, bool):
            self._debug = boolean
        else:
            raise TypeError("debug must be of type bool")



