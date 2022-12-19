import logging
from PIL import Image as PilImage
from PIL import ImageOps, ImageDraw, ImageTk, ImageFont
from tkinter import *
from typing import Callable

from hardware.InterfaceManager import InterfaceManager


class Simulator(Tk):
    """
        Simulator UI used to show an interface for running this application on a local machine
    """
    MAX_WIDTH = 300
    SCALE = 3

    def __init__(self, interface_manager:InterfaceManager, close_event:Callable):
        """ Creates an instance of Simulator
        
        Args:
            interface_manager: The interface manager with all interfaces loaded
            close_event: The function to call when this window is signalled to close
        """
        super().__init__()
        self.resizable(False, False)
        self.title("Zerogen simulator")
        self.protocol("WM_DELETE_WINDOW", self.on_destroy)

        self.interfaces = interface_manager
        self.close_event = close_event

        logging.debug("Generating simulator layout from interfaces..")

        # Calculate interface positions
        self.positions = {}
        self.dimensions = [1, 1]
        x = 1
        y = 10
        max_height = 0
        for interface in interface_manager.interfaces:
            self.positions[interface] = [x, y]

            # Expand dimensions for simulator image cache
            if x + interface.size[0] + 1 > self.dimensions[0]:
                self.dimensions[0] = x + interface.size[0] + 1
            if y + interface.size[1] + 1 > self.dimensions[1]:
                self.dimensions[1] = y + interface.size[1] + 1
            
            # Compute next position
            x += interface.size[0] + 5
            if interface.size[1] > max_height:
                max_height = interface.size[1]

            if x > self.MAX_WIDTH:  # New row
                x = 0
                y += max_height + 15
                max_height = 0
        
        # Generate simulator background
        self.backdrop = PilImage.new("RGB", tuple(self.dimensions), "black")
        backdrop_draw = ImageDraw.Draw(self.backdrop)
        font = ImageFont.load_default()
        for interface in interface_manager.interfaces:
            position = self.positions[interface]
            backdrop_draw.rectangle((
                position[0] - 1,
                position[1] - 1,
                position[0] + interface.size[0],
                position[1] + interface.size[1]
            ), outline="red")
            backdrop_draw.text((position[0], position[1]-12), interface.name, "white", font)

        self.image_label = Label(self)
        self.image_label.pack()
    
    def on_destroy(self):
        logging.warning("Recieved window close event, signaling application")
        self.close_event()
    
    def update(self):
        """ Displays all the interface outputs on the simulator """
        for interface in self.interfaces.interfaces:
            self.backdrop.paste(interface.image, tuple(self.positions[interface]))
        
        # Not very efficent though this is only for development
        if self.SCALE != 1:
            self.image_photo = ImageTk.PhotoImage(ImageOps.scale(self.backdrop, self.SCALE, PilImage.NEAREST))
        else:
            self.image_photo = ImageTk.PhotoImage(self.backdrop)
        
        self.image_label.config(image=self.image_photo)
        super().update()
