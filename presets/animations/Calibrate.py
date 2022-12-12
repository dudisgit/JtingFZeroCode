from animation.IAnimation import IAnimation
from hardware.InterfaceManager import InterfaceManager

class Calibrate(IAnimation):
    """
        Calibration animation for all panels
    """
    def __init__(self, manager:InterfaceManager):
        """ Creates an instance of Calibrate
        
        Args:
            manager: The instance of the interface manager with all it's interfaces loaded
        """
        self.manager = manager

    def start(self):
        pass

    def update(self):
        pass

    def stop(self):
        pass