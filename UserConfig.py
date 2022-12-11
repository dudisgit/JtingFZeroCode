import logging
import pickle
from typing import Dict

from hardware.Configuration import Configuration
from hardware.Interface import Interface

class UserConfig:
    """
        Represents a users configuration, this is normally directed at a binary file for configuration
        Use this class for the following:
            Hardware configuration
            Profiles config
    """
    VERSION = 1

    def __init__(self, config_path:str):
        """ Creates an instance of UserConfig
        
        Args:
            config_path: The full path to user configuration file
        """
        self._filepath = config_path
        logging.info(f"User configuration is at {config_path}")

        self._hardware = {}
        self.interfaces = []
        self.sets = {}
    
    @property
    def hardware(self) -> Dict[str, Configuration]:
        return self._hardware
    
    def load_userconfig(self):
        """ Loads the assigned user configuration into this object """
        logging.debug("Loading user config")

        with open(self._filepath, "rb") as usrFile:
            config = pickle.load(usrFile)

        version = config["Version"]
        logging.debug(f"User config version: {version}")
        
        self.hardware.clear()
        for hardware_config in config["Hardware"]:
            self.hardware[hardware_config["Name"]] = Configuration()
            self.hardware[hardware_config["Name"]].load_from_user_config(hardware_config)
        
        self.interfaces = config["Interfaces"]

    def save_userconfig(self):
        """ Saves the settings in this object to the user configuration file """
        logging.debug("Saving user config")
        
        config = {}
        config["Version"] = self.VERSION

        hardware_configs = {}
        for hardware in self.hardware.values():
            hardware_configs[hardware.name] = hardware.format_as_dictionary()
        config["Hardware"] = hardware_configs
        config["Interfaces"] = self.interfaces

        with open(self._filepath, "wb") as usrFile:
            pickle.dump(config, usrFile)
