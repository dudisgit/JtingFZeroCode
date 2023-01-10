import traceback
from PIL import Image
from hardware.IHardware import IHardware
from hardware.Configuration import Configuration

Import_failure = False
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    Import_failure = True
    traceback.print_exc()

class RpiMatrix(IHardware):
    def __init__(self, config:Configuration):
        assert not Import_failure, "Hardware import failed"

        options = RGBMatrixOptions()
        options.rows = config.args["rows"]
        options.cols = config.args["columns"]
        options.chain_length = config.args["Chain length"]
        options.parallel = config.args["parallel"]
        options.drop_privileges = config.args["Drop privileges"]
        options.hardware_mapping = config.args["Hardware mapping"]
        options.gpio_slowdown = int(config.args["GPIO Slowdown"])
        if config.args["Panel type"]:
            options.panel_type = config.args["Panel type"]

        self.matrix = RGBMatrix(options=options)
        self.image = Image.new("RGB", (self.matrix.width, self.matrix.height), "black")

    @property
    def has_inputs(self) -> bool:
        return False

    @staticmethod
    def new_config() -> Configuration:
        config = Configuration()
        config.hardware_library = "RpiMatrix"
        config.name = "RpiMatrix"
        config.brightness = 100
        config.width = 64
        config.height = 32
        config.args = {
            "rows": 32,
            "columns": 32,
            "Chain length": 4,
            "parallel": 1,
            "Drop privileges": False,
            "Hardware mapping": "adafruit-hat",
            "Panel type": "",
            "GPIO Slowdown": "1"
        }
        config.display_values = {
            "Hardware mapping": {"Type": "Combo", "Values":
                ["regular", "adafruit-hat", "adafruit-hat-pwm", "compute-module"]},
            "GPIO Slowdown": {"Type": "Combo", "Values": ["0", "1", "2", "3", "4"]}
        }
        return config
    
    def update(self):
        self.matrix.SetImage(self.image)

    def teardown(self):
        pass
