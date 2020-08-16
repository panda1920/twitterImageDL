from unittest.mock import patch, Mock

import pytest

from twitter_image_dl.dltask_scheduler import DltaskScheduler
import twitter_image_dl.global_constants as constants

@pytest.fixture(scope='function')
def mocked_subprocess():
    with patch('twitter_image_dl.dltask_scheduler.subprocess', autospec=True) as mock:
        # mock.run = Mock()
        yield mock

class Test_CallsToSubprocess:
    def test_registerShouldCallCreate(self, tmp_path, mocked_subprocess):
        scheduler = DltaskScheduler(tmp_path)
        
        scheduler.register(DltaskScheduler.ScheduleOptions.HOURLY)

        assert len(mocked_subprocess.run.call_args_list) == 1
        # test args passed to subprocess.run()
        args, *_ = mocked_subprocess.run.call_args_list[0][0]
        assert args[0] == 'schtasks.exe'
        assert args[1] == '/Create'

        taskname_postion = args.index('/TN') + 1
        assert args[taskname_postion] == constants.TASKNAME

        taskpath_position = args.index('/TR') + 1
        assert args[taskpath_position] == str(tmp_path / constants.FILENAME_DL)
        
        schedule_position = args.index('/SC') + 1
        assert args[schedule_position] == 'HOURLY'


    def test_deregisterShouldCallDelete(self, tmp_path, mocked_subprocess):
        scheduler = DltaskScheduler(tmp_path)
        
        scheduler.deregister()

        assert len(mocked_subprocess.run.call_args_list) == 1
        # test args passed to subprocess.run()
        args, *_ = mocked_subprocess.run.call_args_list[0][0]
        assert args[0] == 'schtasks.exe'
        assert args[1] == '/Delete'
        assert '/F' in args

        taskname_postion = args.index('/TN') + 1
        assert args[taskname_postion] == DltaskScheduler.TASKNAME
