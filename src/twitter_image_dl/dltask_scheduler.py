from enum import Enum
from pathlib import Path
import subprocess

import twitter_image_dl.global_constants as constants

class DltaskScheduler:
    class ScheduleOptions(Enum):
        MINUTE = 0
        HOURLY = 1
        DAILY  = 2
        WEEKLY = 3
    TASKNAME = constants.TASKNAME

    def __init__(self, app_path):
        self._taskpath = app_path / constants.FILENAME_DL

    def register(self, schedule: ScheduleOptions, options = None):
        if options is None:
            options = {}
        
        self._schedule_task('/Create',
            '/TR', str(self._taskpath),
            '/SC', schedule.name,
            *self._create_starttime_args(options)
        )

    def deregister(self):
        self._schedule_task('/Delete', '/F')

    def _schedule_task(self, op_string, *args):
        subprocess.run(
            ['schtasks.exe', op_string, '/TN', self.TASKNAME, *args],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

    def _create_starttime_args(self, options):
        if constants.START_HOUR not in options:
            return []

        hour = options.get(constants.START_HOUR, 0)
        minute = options.get(constants.START_MINUTE, 0)
        return ['/ST', f'{hour:02}:{minute:02}']
