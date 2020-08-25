import sys

import tkinter as tk
from tkinter import ttk

class TerminalOutput(ttk.Frame):
    """
    Widget that simulates terminal output
    """

    def __init__(self, bindings, master, **config):
        super().__init__(master, **config)
        self._bindings = bindings
        self._initializeWidgets()
        sys.stdout = self

        print('stdout is connected to terminal widget')

    def _initializeWidgets(self):
        self._text = tk.Text(self, wrap='char')
        self._scrollbar = ttk.Scrollbar(self, orient='vertical')
        self._text.configure(yscrollcommand=self._scrollbar.set)
        self._scrollbar.configure(command=self._text.yview)

        self._text.grid(row=0, column=0, sticky='nsew')
        self._scrollbar.grid(row=0, column=1, sticky='ns')
        

    def write(self, msg):
        self._text.configure(state='normal')
        self._text.insert('end', msg)
        self._text.see('end')
        self._text.configure(state='disabled')

    def flush(self):
        pass
