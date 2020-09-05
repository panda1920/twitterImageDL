import tkinter as tk
from tkinter import ttk

class ScheduleSettings(ttk.Frame):
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
        self._schedule_toggled = tk.BooleanVar()
        self._toggle_schedule = ttk.Checkbutton(self,
            text='Register schedule',
            variable=self._schedule_toggled,
            onvalue=True,
            offvalue=False,
        )
        self._schedules = ttk.Combobox(self,
            values=['hourly', 'daily', 'monthly'],
            state='disable'
        )
        self._minutes = tk.Spinbox(self, from_=0, to=59, state='disable')
        self._hours = tk.Spinbox(self, from_=0, to=23, state='disable')

    def _set_widget_geometry(self):
        self._toggle_schedule.grid(row=0, column=0)
        self._schedules.grid(row=1, column=0)
        self._minutes.grid(row=2, column=0)
        self._hours.grid(row=2, column=1)

    def _bind_callbacks(self):
        self._toggle_schedule.configure(command=self._toggle_handler)

    def _load_input_values(self):
        pass

    def _toggle_handler(self, *args):
        if self._schedule_toggled.get():
            self._schedules.configure(state='enable')
            self._minutes.configure(state='normal')
            self._hours.configure(state='normal')
        else:
            self._schedules.configure(state='disable')
            self._minutes.configure(state='disable')
            self._hours.configure(state='disable')

    def _reload_inputs(self):
        self._load_input_values()
        # self._apply_button.configure(state='disabled')
