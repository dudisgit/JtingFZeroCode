from PIL import Image, ImageDraw

from hardware.Types import DisplayForms, HardwareType
from hardware.IHardware import IHardware

class InputInterface:
    """
        Used to represent input interfaces only, this interface is auto generated from hardware config.
        It cannot be defined in the interface config
    """
    def __init__(self, hardware:IHardware):
        """ Creates an instance of Interface
        
        Args:
            hardware: The hardware instance used for this interface
        """
        self.type = HardwareType.Input
        self._hardware = hardware

class Interface:
    """
        Used to represent an interface for controlling full or partial parts of hardware
    """
    def __init__(self, hardware:IHardware):
        """ Creates an instance of Interface
        
        Args:
            hardware: The hardware instance used for this interface
        """
        self.type = HardwareType.Output
        self.form = DisplayForms.Other
        self.name = "Untitled"
        self.size = (1, 1)
        self.image = Image.new("RGB", (1, 1))
        self.draw = ImageDraw.Draw(self.image)

        self._hardware = hardware
    
    def load_from_user_config(self, config:dict):
        """ Loads from the given user configuration dictionary
        
        Args:
            config: The configuration provided from the user config file
        """
        self.name = config["Name"]
        self.form = DisplayForms(config["Form"])
        self.size = tuple(config["Size"])

    def format_as_dict(self) -> dict:
        """ Formats this interfaces config as a dictionary for user config savings
        
        Returns:
            dict: The settings for this interface
        """
        config = {
            "Name": self.name,
            "Form": self.form.value,
            "Size": list(self.size)
        }
        return config
