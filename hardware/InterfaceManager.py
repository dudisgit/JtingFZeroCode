import logging
from typing import List

from hardware.HardwareManager import HardwareManager
from hardware.Interface import Interface, InputInterface
from hardware.Types import HardwareType

class InterfaceManager:
    """
        Interface manager, used to house all interface and provide query methods
    """
    def __init__(self):
        self._interfaces = []
    
    @property
    def interfaces(self) -> List[Interface]:
        return self._interfaces
    
    def initilize_interfaces(self, interfaces:list, manager:HardwareManager):
        """ Initilize all interfaces and attaches them to their equivilent hardware instance
        
        Args:
            interfaces: The interface configuration list provided by the user configuration file
            manager: The hardware manager with all the relavent hardware loaded and ready
        """
        for interface in interfaces:
            instance = Interface(manager.hardware.get(interface["Hardware"], None))
            instance.load_from_user_config(interface)
            self._interfaces.append(instance)
    
    def initilize_input_interfaces(self, manager:HardwareManager):
        """ Initilizes all input interfaces from hardware
        
        Args:
            manager: The hardware manager
        """
        for hardware in manager.hardware.values():
            if hardware.has_inputs:
                self._interfaces.append(InputInterface(hardware))


    #region Animation public methods
    
    def get_interface(self, interface_name:str) -> Interface:
        """ Gets the matching interface instance
        
        Args:
            interface_name: The name of the interface to get (not case sensitive)
        Returns:
            Interface: The found matching interface
            None: The interface wasn't found
        """
        for interface in self.interfaces:
            if interface.name.lower() == interface_name.lower() and interface.type == HardwareType.Output:
                return interface
        return None
    
    def get_interfaces(self, phrase:str) -> List[Interface]:
        """ Gets the matching interface instances via a phrase
        
        Args:
            phrase: The phrase to search for in interface names (not case sensitive)
        Returns:
            List: A list of the found interface instances
        """
        matching = []
        for interface in self.interfaces:
            if phrase.lower() in interface.name.lower() and interface.type == HardwareType.Output:
                matching.append(interface)
        return matching
    
    def get_input_interface(self, interface_name:str) -> InputInterface:
        """ Gets the matching input interface instance
        This interface is not defined in the user made interface config but created by the hardware from config
        
        Args:
            interface_name: The name of the interface
        Returns:
            InputInterface: The found matching interface
            None: The interface wasn't found
        """
        for interface in self.interfaces:
            if interface.name.lower() == interface_name.lower() and interface.type == HardwareType.Input:
                return interface
        return None

    
    #endregion

