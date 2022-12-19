import time
import math
import logging

from animation.IAnimation import IAnimation
from hardware.InterfaceManager import InterfaceManager
from hardware.Types import HardwareType, DisplayForms

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
        self._counter = 0
        self._frame_timer = 0

    def start(self):
        self._counter = 0
        self._frame_timer = time.time() + 1

    def update(self):
        i = math.cos(time.time()*2.5)
        self._counter += 1
        if time.time() > self._frame_timer:
            self._frame_timer = time.time() + 1
            logging.info(f"FPS: {self._counter}")
            self._counter = 0

        for interface in self.manager.interfaces:
            if interface.type != HardwareType.Input:

                if interface.form == DisplayForms.Matrix:
                    interface.draw.rectangle((0, 0)+interface.size, (0, 0, 0))

                    # Draw edges in top left and bottom right corner
                    interface.draw.line((0, 0, 0, 3), (255, 255, 255))
                    interface.draw.line((0, 0, 3, 0), (255, 255, 255))
                    interface.draw.line((interface.size[0]-1, interface.size[1]-1,
                        interface.size[0]-1, interface.size[1]-4), (255, 255, 255))
                    interface.draw.line((interface.size[0]-1, interface.size[1]-1,
                        interface.size[0]-4, interface.size[1]-1), (255, 255, 255))
                    
                    # Animated point to glide accross screen
                    center = (interface.size[0]//2, interface.size[1]//2)
                    interface.draw.line((
                        center[0] + (center[0]*((i*0.9)-0.1)),
                        center[1] + (center[1]*((i*0.9)-0.1)),
                        center[0] + (center[0]*((i*0.9)+0.1)),
                        center[1] + (center[1]*((i*0.9)+0.1))
                    ), (255, 0, 255))

                    # Direction lines
                    interface.draw.line(center+(center[0]+3, center[1]), (0, 255, 0))
                    interface.draw.line(center+(center[0], center[1]-3), (255, 0, 0))

    def stop(self):
        pass
