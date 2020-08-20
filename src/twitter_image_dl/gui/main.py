import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread

from twitter_image_dl.gui.terminal_output import TerminalOutput
from twitter_image_dl.twitterimagedl import dlmedia

class Main:
    """
    Widget that represents the main page of GUI
    """

    def __init__(self, bindings, master, *configs):
        self._bindings = bindings
        self._thread = None
        self._initializeWidgets(master, *configs)

    def _initializeWidgets(self, master, *configs):
        self._main = ttk.Frame(master, *configs)
        self._start_button = ttk.Button(
            self._main, text='download',
            command=self._start_download_background
        )
        self._terminal = TerminalOutput(self._bindings, self._main)

        self._start_button.grid(column=0, row=0)
        self._terminal.grid(column=0, row=1, sticky='nsew')

        # make sure dl task is terminated ASAP when GUI is closed
        self._main.bind('<Destroy>', lambda e:
            self._bindings.get_abort().set_abort()
        )

    def _start_download_background(self):
        if self._thread is not None and self._thread.is_alive():
            return

        self._thread = Thread(target=dlmedia, args=[self._bindings])
        self._thread.start()

    def grid(self, **kwargs):
        self._main.grid(**kwargs)
