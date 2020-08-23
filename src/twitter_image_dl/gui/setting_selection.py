import tkinter as tk
from tkinter import ttk

class SettingSelection(ttk.Frame):
    """
    Combobox to chose which setting criteria to modify
    """
    def __init__(self, bindings, master, selections):
        super().__init__(master)
        self._bindings = bindings
        self._initializeWidgets(selections)

    def _initializeWidgets(self, selections):
        self._selections = tk.StringVar(value=selections)
        self._list = tk.Listbox(self, selectmode='single', height=5, listvariable=self._selections)

        self._list.grid(column=0, row=0, sticky='nsew')
        self._list.bind('<<ListboxSelect>>', self._select_handler)

    def _select_handler(self, event):
        selection = self._list.get( self._list.curselection() )
        if self._selection_callback:
            self._selection_callback(selection)

    def set_selection_callback(self, callback):
        self._selection_callback = callback
