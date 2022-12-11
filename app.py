import logging

from UserConfig import UserConfig
from hardware.HardwareManager import HardwareManager
from hardware.InterfaceManager import InterfaceManager

class App:
    """
        Represents the root zerogen app for controlling hardware and managing animations
    """
    def __init__(self, config:UserConfig):
        """ Creates an instance of App
        
        Args:
            config: The user configuration object loaded with the config
        """
        self.config = config
        self.hardware = HardwareManager()
        self.interfaces = InterfaceManager()
    
    def _load_hardware_and_interfaces(self):
        """ Loads all hardware instances and user interfaces """
        self.hardware.load_hardware(self.config.hardware)
        self.interfaces.initilize_interfaces(self.config.interfaces, self.hardware)
        self.interfaces.initilize_input_interfaces(self.hardware)
