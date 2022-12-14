import logging
import time

from UserConfig import UserConfig
from hardware.HardwareManager import HardwareManager
from hardware.InterfaceManager import InterfaceManager
from animation.AnimationSet import AnimationSet
from exceptions import UnknownSetException

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
        self._set = None
    
    @property
    def set(self) -> AnimationSet:
        return self._set
    
    def load_hardware_and_interfaces(self):
        """ Loads all hardware instances and user interfaces """
        logging.info("Loading all hardware and interfaces")
        self.hardware.load_hardware(self.config.hardware)
        self.interfaces.initilize_interfaces(self.config.interfaces, self.hardware)
        self.interfaces.initilize_input_interfaces(self.hardware)
        logging.debug("Hardware and interfaces created!")
    
    def load_set(self, name:str):
        """ Loads the given set
        
        Args:
            name: The name of the set to load
        """
        if name in self.config.sets:
            if self.set is not None:
                self.set.teardown()

            logging.info(f"Loading set {name}")
            if self._set:
                self.set.teardown()
            self._set = AnimationSet(self.config.sets[name])
            self._set.load_animations(self.interfaces)
        else:
            raise UnknownSetException(f"Unknown set {name}")
    
    def update(self):
        """ Renders the animation and updates all hardware """
        for interface in self.interfaces.interfaces:
            interface.reset_access_flag()

        if self.set is not None and self.set.current_animation is not None:
            self.set.current_animation.update()
        
        for interface in self.interfaces.interfaces:
            if interface.accessed:
                interface.paste_on_hardware()
        
        for hardware in self.hardware.hardware.values():
            hardware.update()

    def teardown(self):
        """ Shuts down all the hardware and closes all the interfaces """
        if self.set:
            self.set.teardown()
        self.hardware.teardown_hardware()

    def mainloop(self, rate:int):
        """ Continuesly runs the update method until the program is terminated
        
        Args:
            rate: Refresh rate in hz to update the app
        """
        while True:
            try:
                next_frame = time.monotonic() + (1/rate)
                self.update()

                delay = next_frame - time.monotonic()
                if delay > 0:
                    time.sleep(delay)
            except KeyboardInterrupt:
                logging.warning("Recieved keyboard interrupt, exiting...")
                self.teardown()
                break
