import tkinter as tk
from tkinter import ttk

import twitter_image_dl.global_constants as cts
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
            cts.IS_SCHEDULED: self._schedule_toggled.get(),
            cts.SCHEDULE_PERIOD: DltaskScheduler.SchedulePeriods[ self._schedules_selections.get() ],
            cts.START_HOUR: self._hours.get(),
            cts.START_MINUTE: self._minutes.get(),
        }
        self._bindings.get_settings().set({ cts.SCHEDULE_SECTION: data })

        # must deregister task that may already by scheduled,
        # so that we can update its settings
        self._bindings.get_scheduler().deregister()

        if data[cts.IS_SCHEDULED]:
            print('Registering download task')
            self._bindings.get_scheduler().register(
                data[cts.SCHEDULE_PERIOD],
                { k: data[k] for k in [cts.START_HOUR, cts.START_MINUTE] }
            )
        else:
            print('Deregistering download task')

    def reload(self):
        self._load_values()
        self._enable_widgets_basedon_toggle()

    def set_onchange_callback(self, callback):
        self._onchange = callback

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
        self._schedules_selections = ttk.Combobox(self._schedules,
            values=self._schedule_intervals,
            state='readonly'
        )

        self._start_time = ttk.Frame(self)
        self._start_time_label = ttk.Label(self._start_time, text='Start time')
        self._hours = tk.IntVar()
        self._hours_label = ttk.Label(self._start_time, text='Hour')
        self._hours_selection = ttk.Spinbox(self._start_time, from_=0, to=23, validate='focus', textvariable=self._hours)
        self._minutes = tk.IntVar()
        self._minutes_label = ttk.Label(self._start_time, text='Minute')
        self._minutes_selection = ttk.Spinbox(self._start_time, from_=0, to=59,
        validate='focus', textvariable=self._minutes)

    def _set_widget_geometry(self):
        self.columnconfigure(0, minsize=18, weight=0)

        self._toggle_schedule.grid(row=0, column=0, columnspan=2, sticky='w')
        
        self._schedules.grid(row=1, column=1, sticky='w')
        self._schedules_label.grid(row=0, column=0, sticky='w')
        self._schedules_selections.grid(row=0, column=1, sticky='w')
        
        self._start_time.grid(row=2, column=1, sticky='w')
        self._start_time.columnconfigure(0, minsize=18, weight=0)
        self._start_time_label.grid(row=0, column=0, columnspan=2, sticky='w')
        self._hours_label.grid(row=1, column=1, sticky='w')
        self._hours_selection.grid(row=1, column=2, sticky='w')
        self._minutes_label.grid(row=1, column=3, sticky='w')
        self._minutes_selection.grid(row=1, column=4, sticky='w')

    def _set_widget_styles(self):
        self._schedules_selections.configure(width=8)
        self._hours_selection.configure(width=4)
        self._minutes_selection.configure(width=4)

        self._schedules_selections.grid(pady=5)
        self._hours_selection.grid(pady=5, padx=(0, 5))
        self._minutes_selection.grid(pady=5, padx=(0, 5))
        self._schedules_label.grid(padx=(0, 5))
        self._hours_label.grid(padx=(0, 5))
        self._minutes_label.grid(padx=(0, 5))

    def _bind_callbacks(self):
        hours_validator = self.register( self._number_mustbe_within(0, 23) )
        hours_default_setter = self._set_default_value(0, self._hours)
        minutes_validator = self.register( self._number_mustbe_within(0, 59) )
        minutes_default_setter = self._set_default_value(0, self._minutes)

        self._toggle_schedule.configure(command=self._toggle_handler)
        self._schedules_selections.bind('<<ComboboxSelected>>', self._onchange_handler)
        self._hours.trace_add('write', self._onchange_handler)
        self._hours_selection.configure(
            validatecommand=(hours_validator, '%P'),
            invalidcommand=hours_default_setter
        )
        self._minutes.trace_add('write', self._onchange_handler)
        self._minutes_selection.configure(
            validatecommand=(minutes_validator, '%P'),
            invalidcommand=minutes_default_setter
        )

    def _number_mustbe_within(self, min, max):
        # min, max is inclusive
        def validator(text):
            if not text.isdigit():
                return False
            return min <= int(text) <= max
            
        return validator

    def _set_default_value(self, default_value, variable):
        def setter(*args):
            variable.set(default_value)
        return setter

    def _load_values(self):
        schedule_settings = self._bindings.get_settings().get()[cts.SCHEDULE_SECTION]
        self._schedules_selections.configure(state='enable')

        self._schedule_toggled.set(schedule_settings[cts.IS_SCHEDULED])
        self._schedules_selections.set(schedule_settings[cts.SCHEDULE_PERIOD].name)
        self._hours.set(schedule_settings[cts.START_HOUR])
        self._minutes.set(schedule_settings[cts.START_MINUTE])

        self._schedules_selections.configure(state='readonly')

    def _enable_widgets_basedon_toggle(self):
        if self._schedule_toggled.get():
            self._schedules_selections.configure(state='readonly')
            self._hours_selection.configure(state='normal')
            self._minutes_selection.configure(state='normal')
        else:
            self._schedules_selections.configure(state='disable')
            self._hours_selection.configure(state='disable')
            self._minutes_selection.configure(state='disable')

    def _toggle_handler(self, *args):
        self._enable_widgets_basedon_toggle()
        self._onchange_handler()

    def _onchange_handler(self, *args):
        if self._onchange:
            self._onchange()
