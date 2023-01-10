from abc import ABCMeta, abstractmethod, abstractproperty
from PIL import Image

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
    
    def __init__(self, config:Configuration):
        """ Creates an instance of the given hardware
        This will import and setup it's bespoke hardware interfaces
        
        Args:
            config: The hardware configuration to load
        """
        # This method exists as only boiler plate and IHardware should never be made an instance
        self.image = Image.new("RGB", (3, 3))

    # Required methods
    
    @abstractmethod
    def new_config() -> Configuration:
        """ Generates a new blank default configuration """
        pass

    @abstractmethod
    def update(self):
        """ Performs an update on the hardware """
        pass

    @abstractmethod
    def teardown(self):
        """ Shuts down the hardware interface """
        pass
