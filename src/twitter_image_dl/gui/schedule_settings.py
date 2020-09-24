import tkinter as tk
from tkinter import ttk

import twitter_image_dl.global_constants as constants
from twitter_image_dl.dltask_scheduler import DltaskScheduler

class ScheduleSettings(ttk.Frame):
    def __init__(self, bindings, master, **config):
        super().__init__(master, **config)
        self._bindings = bindings
        self._schedule_intervals = list( DltaskScheduler.SchedulePeriods.__members__.keys() )
        self._initializeWidgets()

    def lift(self, *args):
        super().lift(*args)

    def apply_change(self):
        data = {
            constants.IS_SCHEDULED: self._schedule_toggled.get(),
            constants.SCHEDULE_PERIOD: DltaskScheduler.SchedulePeriods[ self._schedules_options.get() ],
            constants.START_HOUR: int( self._hours.get() ),
            constants.START_MINUTE: int( self._minutes.get() ),
        }

        self._bindings.get_settings().set({ constants.SCHEDULE_SECTION: data })

    def reload(self):
        self._load_values()

    def _initializeWidgets(self):
        self._create_widgets()
        self._set_widget_geometry()
        self._set_widget_styles()
        self._bind_callbacks()

    def _create_widgets(self):
        self._schedule_toggled = tk.BooleanVar()
        self._toggle_schedule = ttk.Checkbutton(self,
            text='Register schedule',
            variable=self._schedule_toggled,
            onvalue=True,
            offvalue=False,
        )

        self._schedules = ttk.Frame(self)
        self._schedules_label = ttk.Label(self._schedules, text='Execution interval')
        self._schedules_options = ttk.Combobox(self._schedules,
            values=self._schedule_intervals,
        )

        self._start_time = ttk.Frame(self)
        self._start_time_label = ttk.Label(self._start_time, text='Start time')
        self._hours_label = ttk.Label(self._start_time, text='Hour')
        self._hours = tk.Spinbox(self._start_time, from_=0, to=23)
        self._minutes_label = ttk.Label(self._start_time, text='Minute')
        self._minutes = tk.Spinbox(self._start_time, from_=0, to=59)

    def _set_widget_geometry(self):
        self.columnconfigure(0, minsize=18, weight=0)

        self._toggle_schedule.grid(row=0, column=0, columnspan=2, sticky='w')
        
        self._schedules.grid(row=1, column=1, sticky='w')
        self._schedules_label.grid(row=0, column=0, sticky='w')
        self._schedules_options.grid(row=0, column=1, sticky='w')
        
        self._start_time.grid(row=2, column=1, sticky='w')
        self._start_time.columnconfigure(0, minsize=18, weight=0)
        self._start_time_label.grid(row=0, column=0, columnspan=2, sticky='w')
        self._hours_label.grid(row=1, column=1, sticky='w')
        self._hours.grid(row=1, column=2, sticky='w')
        self._minutes_label.grid(row=1, column=3, sticky='w')
        self._minutes.grid(row=1, column=4, sticky='w')

    def _set_widget_styles(self):
        self._schedules_options.configure(width=8)
        self._hours.configure(width=4)
        self._minutes.configure(width=4)

        self._schedules_options.grid(pady=5)
        self._hours.grid(pady=5, padx=(0, 5))
        self._minutes.grid(pady=5, padx=(0, 5))
        self._schedules_label.grid(padx=(0, 5))
        self._hours_label.grid(padx=(0, 5))
        self._minutes_label.grid(padx=(0, 5))

    def _bind_callbacks(self):
        self._toggle_schedule.configure(command=self._toggle_handler)

    def _load_values(self):
        schedule_settings = self._bindings.get_settings().get()[constants.SCHEDULE_SECTION]

        self._schedule_toggled.set(schedule_settings[constants.IS_SCHEDULED])
        self._schedules_options.set(schedule_settings[constants.SCHEDULE_PERIOD].name)
        self._hours.delete(0, 'end')
        self._hours.insert(0, schedule_settings[constants.START_HOUR])
        self._minutes.delete(0, 'end')
        self._minutes.insert(0, schedule_settings[constants.START_MINUTE])

        self._toggle_handler()

    def _toggle_handler(self, *args):
        if self._schedule_toggled.get():
            self._schedules_options.configure(state='enable')
            self._hours.configure(state='normal')
            self._minutes.configure(state='normal')
        else:
            self._schedules_options.configure(state='disable')
            self._hours.configure(state='disable')
            self._minutes.configure(state='disable')
