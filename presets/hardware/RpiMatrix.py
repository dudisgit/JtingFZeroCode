from PIL import Image
from hardware.IHardware import IHardware
from hardware.Configuration import Configuration

from rgbmatrix import RGBMatrix, RGBMatrixOptions

class RpiMatrix(IHardware):
    def __init__(self, config:Configuration):

        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 2
        options.parallel = 1
        options.drop_privileges = False
        options.hardware_mapping = "adafruit-hat"
        self.matrix = RGBMatrix(options=options)
        self.image = Image.new("RGB", (self.matrix.width, self.matrix.height), "black")

    @property
    def has_inputs(self) -> bool:
        return False

    @staticmethod
    def new_config() -> Configuration:
        config = Configuration()
        config.name = "RpiMatrix"
        config.brightness = 100
        config.width = 64
        config.height = 32
        config.args = {
            "rows": 32,
            "chain_length": 4,
            "parallel": 1,
            "drop_privileges": False
        }
        return config
    
    def update(self):
        self.matrix.SetImage(self.image)

    def teardown(self):
        self.image.show()
