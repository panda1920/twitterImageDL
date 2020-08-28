from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog

import twitter_image_dl.global_constants as constants

class GeneralSettings(ttk.Frame):
    def __init__(self, bindings, master, **config):
        super().__init__(master, **config)
        self._bindings = bindings
        self._initializeWidgets()

    def lift(self, *args):
        super().lift(*args)
        self._reload_inputs()
        
    def _initializeWidgets(self):
        self._create_widgets()
        self._set_widget_geometry()
        self._bind_callbacks()
        self._load_input_values()

    def _create_widgets(self):
        self._inputs = {
            'save location': { 
                'label': ttk.Label(self, text='save location: '),
                'entry': ttk.Entry(self),
                'key': constants.SAVE_LOCATION,
            },
        }
        self._save_in_button = ttk.Button(self, text='Save in')
        self._apply_button = ttk.Button(self, text='Apply change', state='disabled')

    def _set_widget_geometry(self):
        for idx, input in enumerate( self._inputs.values() ):
            input['label'].grid(column=0, row=idx, sticky='w')
            input['entry'].grid(column=1, row=idx, sticky='we')
        self._save_in_button.grid(row=0, column=2, sticky='we')
        self._apply_button.grid(row=2, column=2, sticky='we')
        
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

    def _load_input_values(self):
        settings = self._bindings.get_settings().get()

        for input in self._inputs.values():
            input['entry'].insert(
                0, settings[constants.GENERAL_SECTION][input['key']]
            )

    def _bind_callbacks(self):
        for input in self._inputs.values():
            input['entry'].bind('<Key>', lambda e:
                self._apply_button.configure(state='active')
            )
        self._save_in_button.configure(command=self._save_in_handler)
        self._apply_button.configure(command=self._write_widget_values)

    def _save_in_handler(self):
        new_save_location = filedialog.askdirectory(mustexist=True)
        if new_save_location == '':
            return
        
        self._inputs['save location']['entry'].delete(0, 'end')
        self._inputs['save location']['entry'].insert(0, Path(new_save_location))
        self._apply_button.configure(state='active')

    def _write_widget_values(self):
        new_settings = { constants.GENERAL_SECTION: {} }
        general_section = new_settings[constants.GENERAL_SECTION]

        for input in self._inputs.values():
            general_section[input['key']] = input['entry'].get()

        try:
            self._bindings.get_settings().set(new_settings)
            self._bindings.get_settings().write()
            print('Successfuly updated settings file')
        except e as Exception:
            print('Failed to update settings file')
        
    def _reload_inputs(self):
        self._empty_inputs()
        self._load_input_values()
        self._apply_button.configure(state='disabled')

    def _empty_inputs(self):
        for input in self._inputs.values():
            input['entry'].delete(0, 'end')
