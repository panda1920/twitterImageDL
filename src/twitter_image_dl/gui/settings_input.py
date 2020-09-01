import tkinter as tk
from tkinter import ttk

class SettingsInput(ttk.Frame):
    def __init__(self, master, label, key):
        super().__init__(master)
        self._key = key
        self._initializeWidgets(label)

    def get_value(self):
        return self._entry.get()

    def get_key(self):
        return self._key

    def set_value(self, string):
        self._entry.delete(0, 'end')
        self._entry.insert(0, string)

    def set_key_callback(self, callback):
        self._key_callback = callback

    def _initializeWidgets(self, label):
        self._create_widgets(label)
        self._set_widget_geometry()
        self._set_widget_styles()
        self._bind_callbacks()

    def _create_widgets(self, label):
        self._label = ttk.Label(self, text=label)
        self._entry = ttk.Entry(self)

    def _set_widget_geometry(self):
        self._label.grid(row=0, column=0, sticky='w', padx=(0, 10))
        self._entry.grid(row=0, column=1, sticky='we')

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def _set_widget_styles(self):
        self._label.configure(width=15)

    def _bind_callbacks(self):
        self._entry.bind('<Key>', self._key_handler)

    def _key_handler(self, e):
        if self._key_callback:
            self._key_callback(e)
