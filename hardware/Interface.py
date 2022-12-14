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
        self.accessed = False
        self.type = HardwareType.Output
        self.form = DisplayForms.Other
        self.name = "Untitled"
        self.size = (1, 1)
        self.offset = (0, 0)
        self._image = Image.new("RGB", (1, 1))
        self._draw = ImageDraw.Draw(self.image)

        self._hardware = hardware
    
    @property
    def image(self) -> Image.Image:
        """ Returns the PIL image used for this interface """
        self.accessed = True
        return self._image

    @property
    def draw(self) -> ImageDraw.ImageDraw:
        """ Returns the image draw for this interface, use this for PIL drawing functions """
        self.accessed = True
        return self._draw
    
    def reset_access_flag(self):
        """ Resets the access flag used to tell if this interface has been used amoungst an animation """
        self.accessed = False
    
    def paste_on_hardware(self):
        """ Submits the contained image to the assosiated hardware interface """
        if self._hardware:
            self._hardware.image.paste(self._image, self.offset)
            # TODO, check hardware type and turn into strip data if need be

    def load_from_user_config(self, config:dict):
        """ Loads from the given user configuration dictionary
        
        Args:
            config: The configuration provided from the user config file
        """
        self.name = config["Name"]
        self.offset = tuple(config["Offset"])
        self.form = DisplayForms(config["Form"])
        self.size = tuple(config["Size"])
        self._image = Image.new("RGB", self.size)
        self._draw = ImageDraw.Draw(self.image)

    def format_as_dict(self) -> dict:
        """ Formats this interfaces config as a dictionary for user config savings
        
        Returns:
            dict: The settings for this interface
        """
        config = {
            "Name": self.name,
            "Form": self.form.value,
            "Size": list(self.size),
            "Offset": list(self.offset)
        }
        return config
