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

    def _initializeWidgets(self):
        self._create_widgets()
        self._set_widget_geometry()
        self._set_widget_styles()

    def _create_widgets(self):
        self._text = tk.Text(self, wrap='char', state='disabled')
        self._scrollbar = ttk.Scrollbar(self, orient='vertical')
        self._text.configure(yscrollcommand=self._scrollbar.set)
        self._scrollbar.configure(command=self._text.yview)

    def _set_widget_geometry(self):
        self._text.grid(row=0, column=0, sticky='nsew')
        self._scrollbar.grid(row=0, column=1, sticky='ns')

    def _set_widget_styles(self):
        # set whitespaces
        self._text.configure(padx=10, pady=10)

        # set colors
        self._text.configure(background='#3e3e3e', foreground='#ffffff')

    def write(self, msg):
        self._text.configure(state='normal')
        self._text.insert('end', msg)
        self._text.see('end')
        self._text.configure(state='disabled')

    def flush(self):
        pass
