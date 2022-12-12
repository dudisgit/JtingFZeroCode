import logging

from animation.AnimationStatus import AnimationStatus
from animation.IAnimation import IAnimation
from hardware.InterfaceManager import InterfaceManager

class Animation:
    """
        This is used to manage a single animation and it's class instance
    """

    def __init__(self, name:str, manager:InterfaceManager, class_ref:IAnimation=None):
        """ Creates an instance of Animation
        
        Args:
            name: The name of the animation
            manager: An instance of the interface manager, with all the relavent interfaces loaded
            class_ref: (OPTIONAL) The class of the animation to create when started
        """
        self.status = AnimationStatus.Standby

        if class_ref:
            try:
                self._instance = class_ref(manager)
            except:
                logging.exception(f"Failed to create instance of animation for {name}")
                self._instance = None
                self.status = AnimationStatus.Failed
        else:
            self._instance = None
        
        self.name = name
        self.manager = manager
        self.triggers = []
    
    @property
    def instance(self) -> IAnimation:
        return self._instance
    
    def start(self):
        """ Starts the animation """
        if self.status in [AnimationStatus.Failed, AnimationStatus.Disabled]:
            logging.warning(f"Cannot start animation {self.name}, animation is in state {self.status.name}")
            return
        
        if self.instance is not None:
            self.status = AnimationStatus.Running
            self.instance.start()
        
    def update(self):
        """ Call the update method on the animation for continous animations """
        if self.instance:
            self.instance.update()

    def stop(self):
        """ Stops the current animation """
        if self.instance:
            self.status = AnimationStatus.Standby
            self.instance.stop()
        
    def teardown(self):
        """ Tears down the animation """
        if self.instance:
            self.instance.teardown()
            self._instance = None

