import subprocess
from enum import Enum

class DltaskScheduler:
    class ScheduleOptions(Enum):
        MINUTE = 1
        HOURLY = 2
        DAILY  = 3
        WEEKLY = 4
    TASKNAME = 'twitter_image_dl.dltask'

    def register(self, schedule: ScheduleOptions):
        self._schedule_task('/Create', '/SC', schedule.name)

    def deregister(self):
        self._schedule_task('/Delete', '/F')

    def _schedule_task(self, op_string, *args):
        subprocess.run(
            ['schtasks.exe', op_string, '/TN', self.TASKNAME, *args],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
