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

    def register(self, schedule: ScheduleOptions):
        self._schedule_task('/Create',
            '/TR', str(self._taskpath),
            '/SC', schedule.name,
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
