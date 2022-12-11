import logging

from animation.AnimationStatus import AnimationStatus

class Animation:
    def __init__(self):
        self.instance = None
        self.status = AnimationStatus.Standby
        self.triggers = []

