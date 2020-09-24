import tkinter as tk
from tkinter import ttk

import twitter_image_dl.global_constants as constants
from twitter_image_dl.gui.settings_input import SettingsInput

class APISettings(ttk.Frame):
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
        self._bind_callbacks()
        self._load_values()

    def _create_widgets(self):
        self._inputs = {
            SettingsInput(self, 'consumer key:', constants.CONSUMER_KEY),
            SettingsInput(self, 'consumer secret:', constants.CONSUMER_SECRET),
            SettingsInput(self, 'access token:', constants.ACCESS_TOKEN),
            SettingsInput(self, 'access secret:', constants.ACCESS_SECRET),
        }
        self._apply_button = ttk.Button(self, text='Apply change', state='disabled')

    def _set_widget_geometry(self):
        for idx, input in enumerate( self._inputs ):
            input.grid(column=0, row=idx, sticky='we', columnspan=2, pady=2)
        self._apply_button.grid(row=4, column=1, sticky='e')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

    def _load_values(self):
        settings = self._bindings.get_settings().get()

        for input in self._inputs:
            setting_value = settings[constants.API_SECTION][input.get_key()]
            input.set_value(setting_value)

    def _bind_callbacks(self):
        for input in self._inputs:
            input.set_key_callback(lambda e:
                self._apply_button.configure(state='active')
            )

        self._apply_button.configure(command=self._write_widget_values)

    def _write_widget_values(self):
        new_settings = { constants.API_SECTION: {} }
        api_section = new_settings[constants.API_SECTION]

        for input in self._inputs:
            api_section[input.get_key()] = input.get_value()

        try:
            self._bindings.get_settings().set(new_settings)
            self._bindings.get_settings().write()
            print('Successfuly updated settings file')
        except e as Exception:
            print('Failed to update settings file')

    def _reload_inputs(self):
        self._load_values()
        self._apply_button.configure(state='disabled')
