from enum import Enum

class AnimationStatus(Enum):
    Waiting = 0
    Running = 1
    Failed = 2
    Disabled = 3
    Standby = 4
