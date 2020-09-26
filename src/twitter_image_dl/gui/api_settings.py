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

    def apply_change(self):
        new_settings = { constants.API_SECTION: {} }
        api_section = new_settings[constants.API_SECTION]

        for input in self._inputs:
            api_section[input.get_key()] = input.get_value()

        self._bindings.get_settings().set(new_settings)

    def reload(self):
        self._load_values()

    def set_onchange_callback(self, callback):
        self._onchange = callback

    def _initializeWidgets(self):
        self._create_widgets()
        self._set_widget_geometry()
        self._bind_callbacks()
        self._load_values()

    def _create_widgets(self):
        self._inputs = {
            SettingsInput(self, 'Consumer key:', constants.CONSUMER_KEY),
            SettingsInput(self, 'Consumer secret:', constants.CONSUMER_SECRET),
            SettingsInput(self, 'Access token:', constants.ACCESS_TOKEN),
            SettingsInput(self, 'Access secret:', constants.ACCESS_SECRET),
        }

    def _set_widget_geometry(self):
        for idx, input in enumerate( self._inputs ):
            input.grid(column=0, row=idx, sticky='we', columnspan=2, pady=2)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

    def _load_values(self):
        settings = self._bindings.get_settings().get()

        for input in self._inputs:
            setting_value = settings[constants.API_SECTION][input.get_key()]
            input.set_value(setting_value)

    def _bind_callbacks(self):
        for input in self._inputs:
            input.set_key_callback(self._onchange_handler)

    def _onchange_handler(self, *args):
        if self._onchange:
            self._onchange()
