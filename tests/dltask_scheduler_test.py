from unittest.mock import patch, Mock

import pytest

from twitter_image_dl.dltask_scheduler import DltaskScheduler

@pytest.fixture(scope='function')
def mocked_subprocess():
    with patch('twitter_image_dl.dltask_scheduler.subprocess', autospec=True) as mock:
        # mock.run = Mock()
        yield mock

class Test_CallsToSubprocess:
    def test_registerShouldCallCreate(self, mocked_subprocess):
        scheduler = DltaskScheduler()
        
        scheduler.register(DltaskScheduler.ScheduleOptions.HOURLY)

        assert len(mocked_subprocess.run.call_args_list) == 1
        # test args passed to subprocess.run()
        args, *_ = mocked_subprocess.run.call_args_list[0][0]
        assert args[0] == 'schtasks.exe'
        assert args[1] == '/Create'

        taskname_postion = args.index('/TN') + 1
        assert args[taskname_postion] == DltaskScheduler.TASKNAME

        taskpath_position = args.index('/TR') + 1
        assert args[taskpath_position] == str(DltaskScheduler.TASKPATH)
        
        schedule_position = args.index('/SC') + 1
        assert args[schedule_position] == 'HOURLY'


    def test_deregisterShouldCallDelete(self, mocked_subprocess):
        scheduler = DltaskScheduler()
        
        scheduler.deregister()

        assert len(mocked_subprocess.run.call_args_list) == 1
        # test args passed to subprocess.run()
        args, *_ = mocked_subprocess.run.call_args_list[0][0]
        assert args[0] == 'schtasks.exe'
        assert args[1] == '/Delete'
        assert '/F' in args

        taskname_postion = args.index('/TN') + 1
        assert args[taskname_postion] == DltaskScheduler.TASKNAME
