import tkinter as tk
from tkinter import ttk

from twitter_image_dl.gui.general_settings import GeneralSettings
from twitter_image_dl.gui.api_settings import APISettings
from twitter_image_dl.gui.schedule_settings import ScheduleSettings
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
        self._schedule_settings.reload()

    def set_close_callback(self, callback):
        self._close_callback = callback

    def _initializeWidgets(self):
        self._create_widgets()
        self._set_widget_geometry()
        self._bind_callbacks()

    def _create_widgets(self):
        self._apply_change_button = ttk.Button(self, text='Apply Change')
        self._close_button = ttk.Button(self, text='Close')
        self._general_settings = GeneralSettings(self._bindings, self)
        self._schedule_settings = ScheduleSettings(self._bindings, self)
        self._api_settings = APISettings(self._bindings, self)
        self._selections = SettingSelection(self._bindings, self,
            [
                constants.GENERAL_SECTION,
                constants.API_SECTION,
                constants.SCHEDULE_SECTION,
            ]
        )

    def _set_widget_geometry(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

        self._general_settings.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self._api_settings.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self._schedule_settings.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self._selections.grid(row=0, column=0, sticky='nsew', rowspan=2)
        self._apply_change_button.grid(row=1, column=1, sticky='nsew')
        self._close_button.grid(row=2, column=1, sticky='nsew')

    def _bind_callbacks(self):
        self._apply_change_button.configure(command=self._apply_change_handler)
        self._close_button.configure(command=self._close_handler)
        self._selections.set_selection_callback(self._display_setting_page)

    def _apply_change_handler(self):
        self._schedule_settings.apply_change()
        
        try:
            self._bindings.get_settings().write()
            print('Succesfully updated settings file')
        except Exception as e:
            print('Failed to update settings file')

    def _close_handler(self):
        if self._close_callback:
            self._close_callback()

    def _display_setting_page(self, selection):
        if selection == constants.GENERAL_SECTION:
            self._general_settings.lift()
        if selection == constants.API_SECTION:
            self._api_settings.lift()
        if selection == constants.SCHEDULE_SECTION:
            self._schedule_settings.lift()
