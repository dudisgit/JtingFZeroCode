
class Configuration:
    """
        Houses the configuration for a single piece of hardware
    """
    def __init__(self):
        """ Creates an instance of Configuration """
        self.brightness = 100
        self.name = "Unnamed"
        self.args = {}
        self.width = 0
        self.height = 0
        self.display_values = {}  # A dictionary of values that can be displayed on the web UI
        #   These each value is a config describing its apperance, e.g. Int, bool, slider or combo box (with values)
    
    def load_from_user_config(self, config:dict):
        """ Called to load configuration from a dictionary provided from the user config
        
        Args:
            config: The settings provided from the user config
        """
        self.name = config["Name"]
        self.args = config["Arguments"]
        self.brightness = config["Brightness"]
        self.width = config["Width"]
        self.height = config["Height"]

    def format_as_dictionary(self) -> dict:
        """ Formats this configuration in a way that can be saved to the user config
        
        Returns:
            dict: A dictionary with the hardware settings
        """
        config = {
            "Name": self.name,
            "Arguments": self.args,
            "Brightness": self.brightness,
            "Width": self.width,
            "Height": self.height
        }
        return config
