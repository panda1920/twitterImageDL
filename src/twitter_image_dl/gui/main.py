import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread

from twitter_image_dl.gui.terminal_output import TerminalOutput
from twitter_image_dl.twitterimagedl import dlmedia

class MainPage(ttk.Frame):
    """
    Widget that represents the main page of GUI
    """

    def __init__(self, bindings, master, **configs):
        super().__init__(master, **configs)
        self._bindings = bindings
        self._thread = None
        self._initializeWidgets()
        self._bind_callbacks()

    def set_settings_callback(self, callback):
        self._settings_callback = callback

    def _initializeWidgets(self):
        self._start_button = ttk.Button(self, text='download')
        self._settings_button = ttk.Button(self, text='settings')
        self._terminal = TerminalOutput(self._bindings, self)

        self._start_button.grid(row=0, column=0, sticky='ew')
        self._settings_button.grid(row=0, column=1, sticky='ew')
        self._terminal.grid(row=1, column=0, sticky='nsew', columnspan=2)

    def _bind_callbacks(self):
        self._start_button.configure(command=self._start_download_background)
        self._settings_button.configure(command=self._settings_handler)

        # make sure dl task is terminated ASAP when GUI is closed
        self.bind('<Destroy>', lambda e:
            self._bindings.get_abort().set_abort()
        )

    def _settings_handler(self):
        if self._settings_callback:
            self._settings_callback()

    def _start_download_background(self):
        if self._thread is not None and self._thread.is_alive():
            return

        self._thread = Thread(target=dlmedia, args=[self._bindings])
        self._thread.start()
