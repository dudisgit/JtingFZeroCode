import logging
import importlib

from animation.Animation import Animation
from animation.AnimationStatus import AnimationStatus
from hardware.InterfaceManager import InterfaceManager
from exceptions import UnknownAnimationException

class AnimationSet:
    """
        Represents a set containing one or more animations
    """
    def __init__(self, config:dict):
        """ Creates an instance of AnimationSet
        
        Args:
            config: The configuration provided from the user config file
        """
        self._config = config
        self.name = config["Name"]

        self._current_animation = None
        self.animations = {}
    
    def load_animation(self, config:dict, manager:InterfaceManager) -> Animation:
        """ Loads the given animation by the provided config
        
        Args:
            config: The configuration within the user config for the animation
            manager: An instance of the interface manager loaded with all the interfaces
        Returns:
            Animation: The animation instance
        """
        failure = False
        try:
            library = importlib.import_module(config["Path"], config["Package"])
        except:
            logging.exception(f"Failed to load animation {config['Name']}")
            failure = True

        if not failure:
            try:
                class_obj = getattr(library, config["Path"].split(".")[-1])
            except:
                logging.exception(f"Failed to get animation class, have you named it the same as the file?")
                failure = True
        
        if failure:
            anim = Animation(config["Name"], manager)
            anim.status = AnimationStatus.Failed
            return anim
        else:
            anim = Animation(config["Name"], manager, class_obj)
            return anim
        
    def load_animations(self, manager:InterfaceManager):
        """ Create all animation instances within the set, ready for preloading
        
        Args:
            manager: The interface manager
        """
        for animation in self._config["Animations"]:
            logging.debug(f"Loading animation {animation['Name']}")
            self.animations[animation["Name"]] = self.load_animation(animation, manager)
    
    @property
    def current_animation(self) -> Animation:
        return self._current_animation
    
    def change_animation(self, name:str):
        """ Changes the current animation in the set to the specified

        Args:
            name: The name of the animation to load
        """

        if name in self.animations:
            if self.current_animation is not None:
                self.current_animation.stop()
            
            logging.info(f"Changing to animation {name}")
            self._current_animation = self.animations[name]
            self.current_animation.start()
        else:
            raise UnknownAnimationException(f"Unknown animation {name}")

    def teardown(self):
        """ Tears down all animations in this set """
        logging.debug(f"Tearing down animation set of {len(self.animations)} animations('s)")
        for animation in self.animations.values():
            animation.teardown()
