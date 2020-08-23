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

    def _initializeWidgets(self):
        self._create_widgets()
        self._set_widget_positions()
        self._bind_callbacks()

    def _create_widgets(self):
        self._label = ttk.Label(self, text='settings page')
        self._button = ttk.Button(self, text='close', command=lambda:
            self.lower()
        )
        self._general_settings = GeneralSettings(self._bindings, self)
        self._api_settings = APISettings(self._bindings, self)
        self._selections = SettingSelection(self._bindings, self,
            [constants.GENERAL_SECTION, constants.API_SECTION]
        )

    def _set_widget_positions(self):
        self._label.grid(column=0, row=0, columnspan=2)
        self._general_settings.grid(column=1, row=1, sticky='nsew')
        self._api_settings.grid(column=1, row=1, sticky='nsew')
        self._selections.grid(column=0, row=1, sticky='nsew')
        self._button.grid(column=0, row=2, columnspan=2)

    def _bind_callbacks(self):
        self._selections.set_selection_callback(self._display_setting_page)

    def _display_setting_page(self, selection):
        if selection == constants.GENERAL_SECTION:
            self._general_settings.lift()
        if selection == constants.API_SECTION:
            self._api_settings.lift()
