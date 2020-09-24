from enum import Enum
from pathlib import Path
import subprocess
import logging
import json

import twitter_image_dl.global_constants as constants

logger = logging.getLogger(__name__)

class DltaskScheduler:
    class SchedulePeriods(Enum):
        HOURLY = 0
        DAILY  = 1
        WEEKLY = 2
    TASKNAME = constants.TASKNAME

    def __init__(self, app_path):
        logger.info('Initializing task scheduler object')

        self._taskpath = app_path / constants.FILENAME_DL

        logger.info('Finished initializing task scheduler object')

    def register(self, schedule: SchedulePeriods, options = None):
        logger.info('Registering task to schedule')
        logger.debug(
            'executing: %s, schedule : %s, options: %s',
            self._taskpath,
            schedule.name,
            json.dumps(options)
        )
        
        if options is None:
            options = {}
        
        self._schedule_task('/Create',
            '/TR', str(self._taskpath),
            '/SC', schedule.name,
            *self._create_starttime_args(options)
        )

    def deregister(self):
        logger.info('Deregistering task from schedule')

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
