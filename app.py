import logging
import time
import traceback

from UserConfig import UserConfig
from hardware.HardwareManager import HardwareManager
from hardware.InterfaceManager import InterfaceManager
from animation.AnimationSet import AnimationSet
from exceptions import UnknownSetException
try:
    from hardware.Simulator import Simulator
except:
    print("Simulator import failed, simulator is disabled!")
    traceback.print_exc()
    Simulator = None

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
        self._simulator = None
        self._running = True
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
    
    def load_simulator_and_interfaces(self):
        """ Loads up a simulator and user interfaces """
        logging.info("Loading simulator and all interfaces")

        assert Simulator is not None, "Simulator import failed!"
        self.interfaces.initilize_interfaces(self.config.interfaces, self.hardware)
        self.interfaces.initilize_input_interfaces(self.hardware)
        self._simulator = Simulator(self.interfaces, self.signal_terminate)
        
        logging.info("Interfaces created!")
    
    def load_set(self, name:str):
        """ Loads the given animation set
        
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
        
        hardware_accessed = []  # TODO
        for interface in self.interfaces.interfaces:
            if interface.accessed:
                interface.paste_on_hardware()
        
        if self._simulator:
            self._simulator.update()
        else:
            for hardware in self.hardware.hardware.values():
                hardware.update()

    def teardown(self):
        """ Shuts down all the hardware and closes all the interfaces """
        logging.debug("Tearing down all sets and hardware")
        if self.set:
            self.set.teardown()
        self.hardware.teardown_hardware()
        if self._simulator:
            self._simulator.destroy()
    
    def signal_terminate(self):
        """ Signals this application to close and teardown all hardware and interfaes safely """
        logging.debug("Application signalled for termination")
        self._running = False

    def mainloop(self, rate:int):
        """ Continuesly runs the update method until the program is terminated
        
        Args:
            rate: Refresh rate in hz to update the app
        """
        while self._running:
            try:
                next_frame = time.monotonic() + (1/rate)
                self.update()

                delay = next_frame - time.monotonic()
                if delay > 0:
                    time.sleep(delay)
            except KeyboardInterrupt:
                logging.warning("Recieved keyboard interrupt, exiting...")
                self.signal_terminate()

        self.teardown()
