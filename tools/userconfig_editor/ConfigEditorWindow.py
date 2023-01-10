from tkinter import *
from tkinter import ttk

from UserConfig import UserConfig

from tools.userconfig_editor.Hardware import Hardware
from tools.userconfig_editor.Interfaces import Interfaces

class ConfigEditorWindow(Tk):
    """
        Root class for the user config editor app
    """

    def __init__(self):
        """ Creates an instance of ConfigEditorWindow """
        super().__init__()
        self.title("User config editor")

        self.user_config = UserConfig("Untitled.zerouser")

        self._top_bar = Frame(self)
        self._open_button = ttk.Button(self._top_bar, text="Open")
        self._open_button.pack(side=LEFT)
        self._save_button = ttk.Button(self._top_bar, text="Save")
        self._save_button.pack(side=LEFT)
        self.config_label = Label(self._top_bar, text="Untitled")
        self.config_label.pack(side=LEFT)
        self._top_bar.pack(side=TOP, fill=X)

        self.sections = ttk.Notebook(self)

        self.hardware = Hardware(self.sections, self.user_config)
        self.sections.add(self.hardware, text="Hardware")

        self.interfaces = Interfaces(self.sections)
        self.sections.add(self.interfaces, text="Interfaces")

        self.sections.pack(side=BOTTOM, fill=BOTH, expand=True)

