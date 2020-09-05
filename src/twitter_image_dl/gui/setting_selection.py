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

    def select(self, index):
        self._list.selection_clear(0, 'end')
        self._list.selection_set(index)
        self._list.activate(index)
        self._list.event_generate('<<ListboxSelect>>')

    def set_selection_callback(self, callback):
        self._selection_callback = callback

    def _initializeWidgets(self, selections):
        self._selections = tk.StringVar(value=selections)
        self._list = tk.Listbox(self, selectmode='single', listvariable=self._selections)

        self._list.grid(row=0, column=0, sticky='nsew')
        self.rowconfigure(0, weight=1)
        self._list.bind('<<ListboxSelect>>', self._select_handler)

        # set styles
        for i in range(len(selections)):
            if i % 2 == 1:
                self._list.itemconfigure(i, background='#e0e0e0')

        self._list.configure(activestyle='none', highlightthickness=0)
        self._list.bind('<Tab>', lambda *args: 'break') # don't want the widget to respond to tab

    def _select_handler(self, event):
        selection = self._list.get( self._list.curselection() )
        if self._selection_callback:
            self._selection_callback(selection)
