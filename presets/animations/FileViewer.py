from animation.IAnimation import IAnimation
from hardware.InterfaceManager import InterfaceManager

class FileViewer(IAnimation):
    """
        File playback animation, used to display static images or animated clips
    """
    def __init__(self, manager:InterfaceManager):
        """ Creates an instance of FileViewer
        
        Args:
            manager: The instance of the interface manager with all it's interfaces loaded
        """
        self.manager = manager
        # TODO
        #   Store interfaces used and segment positions in seperate file
        #   Use image loader, or video playback, must conserve RAM
        #   Patial interfaces an be used for animation
    
    def start(self):
        pass

    def update(self):
        pass

    def stop(self):
        pass
