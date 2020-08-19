import tkinter as tk
import tkinter.ttk as ttk

class Main:
    """
    Widget that represents the main page of GUI
    """

    def __init__(self, bindings, master, *configs):
        self._bindings = bindings
        self._initializeWidgets(master, *configs)

    def _initializeWidgets(self, master, *configs):
        self._main = ttk.Frame(master, *configs)
        self._start_button = ttk.Button(self._main, text='start')
        self._terminal = ttk.Frame(self._main)

        self._start_button.grid(column=0, row=0)
        self._terminal.grid(column=0, row=1, sticky='nsew')

    def grid(self, **kwargs):
        self._main.grid(**kwargs)
