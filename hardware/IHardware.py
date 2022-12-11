from abc import ABCMeta, abstractmethod, abstractproperty
from hardware.Types import DisplayForms
from hardware.Configuration import Configuration

class IHardware(metaclass=ABCMeta):
    """
        Interface class used for hardware
    """
    @property
    @abstractproperty
    def has_inputs(self) -> bool:
        """ Returns true if this hardware interface has input functionality """
        pass
    
    @abstractmethod
    def new_config() -> Configuration:
        """ Generates a new blank default configuration """
        pass

    @abstractmethod
    def teardown(self):
        """ Shuts down the hardware interface """
        pass
