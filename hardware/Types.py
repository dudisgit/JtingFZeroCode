from enum import Enum

class DisplayForms(Enum):
    Other = 0
    Matrix = 1
    Strip = 2
    Pixel = 3

class HardwareType(Enum):
    Input = 0
    Output = 1
    InputOutput = 2
