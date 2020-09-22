import tkinter as tk
from tkinter import ttk

class SettingSelection(ttk.Frame):
    """
    Listbox to chose which setting criteria to modify
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

        self._set_widget_geometry()
        self._set_widget_styles()
        self._bind_callbacks()

    def _set_widget_geometry(self):
        self._list.grid(row=0, column=0, sticky='nsew')
        self.rowconfigure(0, weight=1)

    def _set_widget_styles(self):
        self._set_selection_colors()
        self._list.configure(activestyle='none', highlightthickness=0)

    def _bind_callbacks(self):
        self._list.bind('<<ListboxSelect>>', self._select_handler)
        self._list.bind('<Tab>', lambda *args: 'break') # don't want the widget to respond to tab

    def _set_selection_colors(self):
        for i in range( self._list.size() ):
            if i % 2 == 0:
                color = ''
            else:
                color = '#e0e0e0'
            self._list.itemconfigure(i, bg=color, fg='')

    def _select_handler(self, event):
        selection_index = self._list.curselection()
        if not selection_index:
            # do nothing when focus moves out of selection widget
            return

        self._set_selection_colors()
        self._list.itemconfig(selection_index, bg='SystemHighlight', fg='SystemHighlightText')

        if self._selection_callback:
            self._selection_callback( self._list.get( selection_index ) )
