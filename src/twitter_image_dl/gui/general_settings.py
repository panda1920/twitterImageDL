from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog

import twitter_image_dl.global_constants as constants
from twitter_image_dl.gui.settings_input import SettingsInput

class GeneralSettings(ttk.Frame):
    def __init__(self, bindings, master, **config):
        super().__init__(master, **config)
        self._bindings = bindings
        self._initializeWidgets()

    def lift(self, *args):
        super().lift(*args)
        self._reload_inputs()
        
    def _initializeWidgets(self):
        self._create_widgets()
        self._set_widget_geometry()
        # self._set_widget_styles()
        self._bind_callbacks()
        self._load_input_values()

    def _create_widgets(self):
        self._inputs = [
            SettingsInput(self, 'save location:', constants.SAVE_LOCATION),
        ]
        self._save_in_button = ttk.Button(self, text='Save in')
        self._apply_button = ttk.Button(self, text='Apply change', state='disabled')

    def _set_widget_geometry(self):
        for idx, input in enumerate( self._inputs ):
            input.grid(column=0, row=idx, sticky='we', columnspan=2, pady=2)
        self._save_in_button.grid(row=0, column=2, sticky='we', pady=2)
        self._apply_button.grid(row=1, column=2, sticky='we')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def _load_input_values(self):
        settings = self._bindings.get_settings().get()

        for input in self._inputs:
            setting_value = settings[constants.GENERAL_SECTION][input.get_key()]
            input.set_value(setting_value)

    def _set_widget_styles(self):
        self.grid(padx=10, pady=10)

    def _bind_callbacks(self):
        for input in self._inputs:
            input.set_key_callback(lambda e:
                self._apply_button.configure(state='active')
            )
        self._save_in_button.configure(command=self._save_in_handler)
        self._apply_button.configure(command=self._write_widget_values)

    def _save_in_handler(self):
        new_save_location = filedialog.askdirectory(mustexist=True)
        if new_save_location == '':
            return
        
        self._inputs[0].set_value(Path(new_save_location))
        self._apply_button.configure(state='active')

    def _write_widget_values(self):
        new_settings = { constants.GENERAL_SECTION: {} }
        general_section = new_settings[constants.GENERAL_SECTION]

        for input in self._inputs:
            general_section[input.get_key()] = input.get_value()

        try:
            self._bindings.get_settings().set(new_settings)
            self._bindings.get_settings().write()
            print('Successfuly updated settings file')
        except e as Exception:
            print('Failed to update settings file')
        
    def _reload_inputs(self):
        self._load_input_values()
        self._apply_button.configure(state='disabled')
