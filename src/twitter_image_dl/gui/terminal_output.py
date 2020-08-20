import sys

import tkinter as tk
from tkinter import ttk

class TerminalOutput:
    """
    Widget that simulates terminal output
    """

    def __init__(self, bindings, master, *config):
        self._bindings = bindings
        self._initializeWidgets(master, *config)
        # sys.stdout = self

        print('stdout is connected to terminal widget')

    def _initializeWidgets(self, master, *config):
        self._terminal = ttk.Frame(master, *config)
        self._text = tk.Text(self._terminal, width=30, height=10, wrap='char')
        self._scrollbar = ttk.Scrollbar(self._terminal, orient='vertical')

        self._text.grid(column=0, row=0)
        self._scrollbar.grid(column=1, row=0)
        print(self._text.configure().keys())

    def grid(self, **kwargs):
        self._terminal.grid(**kwargs)

    def write(self, msg):
        self._text.configure(state='normal')
        self._text.insert('end', msg)
        self._text.configure(state='disabled')

    def flush(self):
        pass
