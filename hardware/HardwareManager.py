import logging
import os
import importlib
from typing import List, Dict

from hardware.Configuration import Configuration
from hardware.IHardware import IHardware
from exceptions import UnknownHardwareException

class HardwareManager:
    """
        This class is used to manage all the hawrware used on the protogen
        It can be used to query for interfaces and setup the hardware instances
    """

    def __init__(self):
        self._hardware = {}
        self.availible_hardware = []
    
    @property
    def hardware(self) -> Dict[str, IHardware]:
        return self._hardware
    
    def teardown_hardware(self):
        """ Closes down all the hardware managed by this manager """
        for hardware in self.hardware.values():
            hardware.teardown()
    
    def get_default_config(self, name:str) -> Configuration:
        """ Gets the default configuration for the specified hardware
        Use this for setting up new hardware interfaces
        
        Args:
            name: The name of the library to load
        Returns:
            Configuration: A base configuration for the hardware
        """
        try:
            library = importlib.import_module(f"presets.hardware.{name}")
        except:
            logging.exception(f"Failed to import hardware interface {name}")
            return
        
        try:
            hardware_object = getattr(library, name)
        except:
            logging.exception(f"Failed to find hardware class {name} in file")
            return
        
        return hardware_object.new_config()
    
    def load_hardware_instance(self, name:str, config:Configuration):
        """ Loads the specified hardware
        
        Args:
            name: The name of the library to load
            config: The configuration to apply to the library
        """
        try:
            library = importlib.import_module(f"presets.hardware.{name}")
        except:
            logging.exception(f"Failed to import hardware interface {name}")
            return
        
        try:
            instance = getattr(library, name)(config)
        except:
            logging.exception(f"Failed to load hardware interface {name}")
            return

        self._hardware[name] = instance
    
    def load_hardware(self, hardware_devices:Dict[str, Configuration]):
        """ Initilizes all the hardware instances from the user configuration
        
        Args:
            hardware_devices: A dictionary of hardware configurations
        Raises:
            UnknownHardwareException: A hardware device in config is unknown
        """
        self.availible_hardware = []
        preset_hardware = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presets", "hardware")
        for file in os.listdir(preset_hardware):
            if file.endswith(".py"):
                self.availible_hardware.append(file.strip(".py"))

        for config in hardware_devices.values():
            name = config.hardware_library
            if name in self.availible_hardware:
                try:
                    library = importlib.import_module(f"presets.hardware.{name}")
                except:
                    logging.exception(f"Failed to import hardware interface {name}")
                    continue
                
                try:
                    instance = getattr(library, name)(config)
                except:
                    logging.exception(f"Failed to load hardware interface {name}")
                    continue

                self._hardware[config.name] = instance
            else:
                raise UnknownHardwareException(f"Unkown hardware library {name}")

