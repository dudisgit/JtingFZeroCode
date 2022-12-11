from hardware.IHardware import IHardware
from hardware.Configuration import Configuration

class RpiMatrix(IHardware):
    def __init__(self, config:Configuration):
        pass

    @staticmethod
    def new_config() -> Configuration:
        config = Configuration()
        config.name = "RpiMatrix"
        config.brightness = 100
        config.args = {
            "rows": 32,
            "chain_length": 4,
            "parallel": 1,
            "drop_privileges": False
        }
        return config

    def shutdown(self):
        pass