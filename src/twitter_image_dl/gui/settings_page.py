import tkinter as tk
from tkinter import ttk

from twitter_image_dl.gui.general_settings import GeneralSettings
from twitter_image_dl.gui.api_settings import APISettings
from twitter_image_dl.gui.setting_selection import SettingSelection
import twitter_image_dl.global_constants as constants

class SettingsPage(ttk.Frame):
    """
    Widget to allow configuration of app settings
    """
    def __init__(self, bindings, master, **config):
        super().__init__(master, **config)
        self._bindings = bindings
        self._initializeWidgets()

    def lift(self, *args):
        super().lift(*args)
        self._selections.select(0)

    def set_close_callback(self, callback):
        self._close_callback = callback

    def _initializeWidgets(self):
        self._create_widgets()
        self._set_widget_geometry()
        self._bind_callbacks()

    def _create_widgets(self):
        self._label = ttk.Label(self, text='settings page')
        self._close_button = ttk.Button(self, text='close')
        self._general_settings = GeneralSettings(self._bindings, self)
        self._api_settings = APISettings(self._bindings, self)
        self._selections = SettingSelection(self._bindings, self,
            [constants.GENERAL_SECTION, constants.API_SECTION]
        )

    def _set_widget_geometry(self):
        self._label.grid(row=0, column=0, columnspan=2)
        self._general_settings.grid(row=1, column=1, sticky='nsew')
        self._api_settings.grid(row=1, column=1, sticky='nsew')
        self._selections.grid(row=1, column=0, sticky='nsew', rowspan=2)
        self._close_button.grid(row=2, column=1, sticky='sew')
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def _bind_callbacks(self):
        self._close_button.configure(command=self._close_handler)
        self._selections.set_selection_callback(self._display_setting_page)

    def _close_handler(self):
        if self._close_callback:
            self._close_callback()

    def _display_setting_page(self, selection):
        if selection == constants.GENERAL_SECTION:
            self._general_settings.lift()
        if selection == constants.API_SECTION:
            self._api_settings.lift()
