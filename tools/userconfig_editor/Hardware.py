import importlib
import logging

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from UserConfig import UserConfig

from hardware.HardwareManager import HardwareManager
from hardware.Configuration import Configuration

class ConfigurationArea(LabelFrame):
    """
        Presents the user with the hardware config through generated UI elements
    """
    def __init__(self, master: Frame):
        super().__init__(master, text="Configuration")

        self.custom_fields = LabelFrame(self, text="Custom fields")
        self.custom_fields.pack(side=BOTTOM, anchor=N, fill=BOTH)

        self.elements = {}
    
    def _new_value_changer(self, master:Frame, name:str, value:any, ranges:dict={}) -> Frame:
        """ Creates a frame with a name and value pair
        
        Args:
            master: The master tkitner frame to create a child from
            name: The name applied to the variable
            value: The current value of the variable
            ranges: (OPTIONAL) Specifies any ranges for values
        """
        frame = Frame(master)
        frame.value_label = Label(frame, text=name.capitalize())
        frame.value_label.pack(side=LEFT)

        if type(value) is str:
            if ranges:
                if ranges["Type"] == "Combo":
                    frame.value_instance = StringVar(frame)
                    frame.value_changer = ttk.Combobox(frame, textvariable=frame.value_instance)
                    frame.value_changer["values"] = ranges["Values"]
                    frame.value_instance.set(value)
            else:
                frame.value_instance = StringVar(frame)
                frame.value_changer = Entry(frame, textvariable=frame.value_instance)
                frame.value_instance.set(value)

        elif type(value) is int:
            if ranges:
                if ranges["Type"] == "Slider":
                    frame.value_instance = IntVar(frame)
                    frame.value_changer = ttk.LabeledScale(
                        frame,
                        from_=ranges["Start"],
                        to=ranges["End"],
                        variable=frame.value_instance
                    )
                    frame.value_instance.set(value)
                elif ranges["Type"] == "Range":
                    frame.value_instance = IntVar(frame)
                    frame.value_changer = ttk.Spinbox(
                        frame,
                        from_=ranges["Start"],
                        to=ranges["End"],
                        textvariable=frame.value_instance
                    )
                    frame.value_instance.set(value)
            else:
                frame.value_instance = IntVar(frame)
                frame.value_changer = ttk.Spinbox(
                    frame,
                    from_=0,
                    to=9999,
                    textvariable=frame.value_instance
                )
                frame.value_instance.set(value)
        
        elif type(value) is bool:
            frame.value_instance = IntVar(frame)
            frame.value_changer = ttk.Checkbutton(frame, variable=frame.value_instance)
            frame.value_instance.set(value)
        
        frame.value_changer.pack(side=RIGHT, fill=X, expand=True)
        return frame
    
    def load_config(self, config:Configuration):
        """ Loads the given hardware configuration
        
        Args:
            config: The hardware configuration instance to load
        """
        self.clear_elements()

        self.elements["hardware"] = Label(self, text=f"Hardware library: {config.hardware_library}")
        self.elements["hardware"].pack(side=TOP, anchor=W)
        self.elements["name"] = self._new_value_changer(self, "Name", config.name)
        self.elements["name"].pack(side=TOP, anchor=W, fill=X)
        self.elements["brightness"] = self._new_value_changer(self, "Brightness", config.brightness,
            {"Type": "Slider", "Start": 0, "End": 100})
        self.elements["brightness"].pack(side=TOP, anchor=W, fill=X)
        self.elements["width"] = self._new_value_changer(self, "Width", config.width)
        self.elements["width"].pack(side=TOP, anchor=W, fill=X)
        self.elements["height"] = self._new_value_changer(self, "Height", config.height)
        self.elements["height"].pack(side=TOP, anchor=W, fill=X)

        for argument, value in config.args.items():
            self.elements[f"arg_{argument}"] = self._new_value_changer(
                self.custom_fields,
                argument,
                value,
                config.display_values.get(argument, {})
            )
            self.elements[f"arg_{argument}"].pack(side=TOP, anchor=W, fill=X)

        self.update()
    
    def save_to_config(self, config:Configuration, hardware) -> bool:
        """ Saves the current values to the specified config
        Any errors will be raised as a dialog and returned
        
        Args:
            config: The configuration object to adjust
            hardware: The Hardware UI Frame instance
        Returns:
            bool: If the config was successfuly saved
        """
        # Config name
        new_name = self.elements["name"].value_instance.get()
        if config.name != new_name:  # Update name
            if new_name in hardware.user_config.hardware:
                messagebox.showerror("Hardware config name", "New hardware config name already exists!")
                return False
            
            if len(new_name) == 0:
                messagebox.showerror("Hardware config name", "Hardware name cannot be empty!")
                return False

            hardware.user_config.hardware[new_name] = hardware.user_config.hardware.pop(config.name)
            config.name = new_name
            hardware.refresh_hardware_list()

            # TODO
            #  Fire event that makes interfaces ann all such linked components rename
        
        for intvar in ["brightness", "width", "height"]:
            try:
                int(self.elements[intvar].value_instance.get())
            except:
                messagebox.showerror("Value error", f"Value {intvar} does not conform to an ingeter")
                return False

        # Config brightness
        brightness = int(self.elements["brightness"].value_instance.get())
        if brightness < 0 or brightness > 100:
            messagebox.showerror("Brightness", "The brightness is out of range!")
            return False
        config.brightness = brightness

        # Config width
        width = int(self.elements["width"].value_instance.get())
        if width < 1:
            messagebox.showerror("Width", "Width cannot be less than 1")
            return False
        config.width = width

        # Config height
        height = int(self.elements["height"].value_instance.get())
        if height < 1:
            messagebox.showerror("Height", "Height cannot be less than 1")
            return False
        config.height = height

        # Custom fields
        for argument in config.args:
            value = self.elements[f"arg_{argument}"].value_instance.get()

            if argument in config.display_values:
                rules = config.display_values[argument]

                if rules["Type"] in ["Slider", "Range"]:
                    if value < rules["Start"] or value > rules["End"]:
                        messagebox.showerror(f"Custom field {argument}",
                            f"Value cannot be outside range of {rules['Start']}-{rules['End']}")
                        return False
                    
                elif rules["Type"] == "Combo":
                    if value not in rules["Values"]:
                        messagebox.showerror(f"Custom field {argument}",
                            f"Value selected not in combo box list")
                        return False

            try:
                type(config.args[argument])(value)
            except ValueError:
                messagebox.showerror("Value error",
                    f"Failed to convert custom field {argument} to {type(config.args[argument])}")
                return False
            config.args[argument] = type(config.args[argument])(value)

        return True
    
    def config_changed(self, config:Configuration) -> bool:
        """ Detects changes between the interface values and the pre-config
        
        Args:
            config: The orignial config that populated the interface
        Returns:
            bool: If any values changed in the config
        """
        if str(self.elements["name"].value_instance.get()) != str(config.name):
            return True
        if str(self.elements["brightness"].value_instance.get()) != str(config.brightness):
            return True
        if str(self.elements["height"].value_instance.get()) != str(config.height):
            return True
        if str(self.elements["width"].value_instance.get()) != str(config.width):
            return True
        
        # Custom fields
        for argument in config.args:
            value = self.elements[f"arg_{argument}"].value_instance.get()
            try:
                type(config.args[argument])(value)
            except ValueError:
                return True
            
            if type(config.args[argument])(value) != config.args[argument]:
                return True
        
        return False
    
    def clear_elements(self):
        """ Deletes all UI elements in the configuration area """
        for element in self.elements.values():
            element.destroy()
        self.elements.clear()


class Hardware(Frame):
    """
        This is used to add and modify existing hardware in the user config
    """

    def __init__(self, master: Frame, user_config:UserConfig):
        """ Creates an instance of Hardware
        
        Args:
            master: The master tkinter object
            user_config: The user configruation object to interface with
        """
        super().__init__(master)
        self.user_config = user_config

        self.hardware = self.get_hardware_imports()
        self.current_hardware = None
        self.manager = HardwareManager()

        # Hardware adding
        self._add_frame = Frame(self)
        self.hardware_selection = StringVar(self)
        self.hardware_selector = ttk.Combobox(
            self._add_frame,
            textvariable=self.hardware_selection
        )
        self.hardware_selector["values"] = list(self.hardware)
        self.hardware_selector.pack(side=LEFT)
        self._add_hardware_button = ttk.Button(self._add_frame, text="Add", command=self.add_hardware)
        self._add_hardware_button.pack(side=RIGHT)
        self._add_frame.pack(side=TOP, anchor=W)
        
        self._bottom_frame = Frame(self)
        # Hardware list
        self._selector_frame = Frame(self._bottom_frame)

        self._selector_inner_frame = Frame(self._selector_frame)
        self._current_hardware_list_scroll = ttk.Scrollbar(self._selector_inner_frame)
        self.current_hardware_list = Listbox(self._selector_inner_frame, width=25, yscrollcommand=self._current_hardware_list_scroll.set)
        self.current_hardware_list.pack(side=LEFT, fill=Y, expand=True)
        self._current_hardware_list_scroll.config(command=self.current_hardware_list.yview)
        self._current_hardware_list_scroll.pack(side=RIGHT, fill=Y)
        self._selector_inner_frame.pack(side=TOP, fill=Y, expand=True)

        self.current_hardware_list.bind("<Button-1>", lambda *ev: self.after(10, self.open_hardware))
        self._remove_hardware_button = ttk.Button(self._selector_frame, text="Delete", command=self.delete_selected)
        self._remove_hardware_button.pack(side=BOTTOM)
        self._selector_frame.pack(side=LEFT, fill=Y)

        # Hardware config
        self._config_area_frame = Frame(self._bottom_frame)
        self.hardware_config = ConfigurationArea(self._config_area_frame)
        self.hardware_config.pack(side=TOP, fill=BOTH, expand=True)
        self._save_button = ttk.Button(self._config_area_frame, text="Apply", command=self.save_hardware_settings)
        self._save_button.pack(side=BOTTOM)
        self._config_area_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self._bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
    
    def delete_selected(self):
        """ Called to delete the currently selected hardware item """
        if self.current_hardware:
            if messagebox.askyesno("Delete hardware", f"Are you sure you want to delete {self.current_hardware.name}?"):
                self.user_config.hardware.pop(self.current_hardware.name)
                self.current_hardware = None
                self.hardware_config.clear_elements()
                self.refresh_hardware_list()
    
    def add_hardware(self):
        """ Adds the selected hardware to the user config """
        selection = self.hardware_selection.get()
        
        if selection in self.hardware:
            if selection in self.user_config.hardware:
                messagebox.showerror("Add hardware", f"Hardware {selection} already exists!\nPlease re-name it before adding more")
                return
            
            if self.current_hardware and self.hardware_config.config_changed(self.current_hardware):
                if not messagebox.askyesno("Add hardware", "Unsaved changes currently in the editor, disregard changes to hardware?"):
                    return
            
            config = self.manager.get_default_config(self.hardware[selection])

            if config:
                self.current_hardware_list.insert(END, selection)
                self.user_config.hardware[config.name] = config
                self.current_hardware = config
                self.hardware_config.load_config(config)

                self.current_hardware_list.selection_clear(0, END)
                self.current_hardware_list.selection_set(END)
        else:
            messagebox.showerror("Selection", "Unknown/no hardware module selected")
    
    def save_hardware_settings(self):
        """ Called to save the current hardware settings to the interface """
        if self.current_hardware:
            self.hardware_config.save_to_config(self.current_hardware, self)
    
    def open_hardware(self):
        """ Called when hardware was selected in the hardware selector list """
        try:
            hardware = self.current_hardware_list.selection_get()
        except:
            hardware = None
        
        if hardware:
            if self.current_hardware == self.user_config.hardware[hardware]:
                return
            
            if self.current_hardware and self.hardware_config.config_changed(self.current_hardware):
                question = messagebox.askyesnocancel(
                    "Change hardware",
                    "You have made changes to the hardware, do you want to save them?"
                )
                reset = False

                if question is None:
                    reset = True
                elif question:
                    if not self.hardware_config.save_to_config(self.current_hardware, self):
                        reset = True
                
                if reset:
                    self.current_hardware_list.selection_clear(0, END)
                    self.current_hardware_list.selection_set(
                        list(self.user_config.hardware.values()).index(self.current_hardware)
                    )
                    return
                
            self.current_hardware = self.user_config.hardware[hardware]
            self.hardware_config.load_config(self.current_hardware)

    def refresh_hardware_list(self):
        """ Clears and repopulates the hardware list """
        self.current_hardware_list.delete(0, END)
        for hardware in self.user_config.hardware:
            self.current_hardware_list.insert(END, hardware)

    def get_hardware_imports(self) -> dict:
        """ Gets all availible hardware modules
        
        Returns:
            dict: A dictionary with all hardware module names along with their module path
        """
        # TODO, make dynamic
        hardware_list = {
            "RpiMatrix": "RpiMatrix"
        }

        return hardware_list



