from pathlib import Path
from unittest.mock import create_autospec
import shutil
import sys

import pytest
    
from twitter_image_dl.twitterimagedl import dlmedia
from twitter_image_dl.runtime_bindings import RuntimeBindings
from twitter_image_dl.download_history import DownloadHistory
from twitter_image_dl.settings import Settings
from twitter_image_dl.abort_flag import AbortFlag
import twitter_image_dl.exceptions as exceptions
import twitter_image_dl.global_constants as constants

PROJECT_DIR = Path(__file__).resolve().parents[1]
TEST_DL_LOCATION = PROJECT_DIR / 'testdata' / 'download'

@pytest.fixture(scope='function', autouse=True)
def cleanupTestDL():
    for f in TEST_DL_LOCATION.iterdir():
        if f.is_file():
            f.unlink()
        elif f.is_dir():
            shutil.rmtree(f)

sysArgs = []
@pytest.fixture(scope='function', autouse=True)
def restoreSysArgs():
    sysArgs = sys.argv
    yield
    sys.argv = sysArgs

@pytest.fixture(scope='function')
def use_test_settings():
    test_settings = PROJECT_DIR / 'testdata' / 'settings' / constants.FILENAME_SETTINGS
    copied_settings = PROJECT_DIR / constants.FILENAME_SETTINGS
    shutil.copyfile(test_settings, copied_settings)

    yield

    copied_settings.unlink()

@pytest.fixture(scope='function')
def mock_bindings():
    bindings = create_autospec(RuntimeBindings)
    bindings.get_settings.return_value = create_autospec(Settings)
    bindings.get_history.return_value = create_autospec(DownloadHistory)
    bindings.get_abort.return_value = create_autospec(AbortFlag)
    bindings.get_abort.return_value.is_set.return_value = False
    bindings.get_save_location.return_value = TEST_DL_LOCATION

    return bindings

def test_dlmediaShouldValidateSettings(mock_bindings):
    mock_settings = mock_bindings.get_settings.return_value

    dlmedia(mock_bindings)

    assert len(mock_settings.validate_settings.call_args_list) == 1

def test_dlmediaShouldLoadFromHistoryFile(mock_bindings):
    mock_history = mock_bindings.get_history.return_value

    dlmedia(mock_bindings)

    assert len(mock_history.loadFromFile.call_args_list) == 1
    filepath, *_ = mock_history.loadFromFile.call_args_list[0][0]
    assert filepath == TEST_DL_LOCATION / constants.FILENAME_HISTORY
    
def test_dlmediaShouldWriteToHistoryFile(mock_bindings):
    mock_history = mock_bindings.get_history.return_value

    dlmedia(mock_bindings)

    assert len(mock_history.writeToFile.call_args_list) == 1
    filepath, *_ = mock_history.writeToFile.call_args_list[0][0]
    assert filepath == TEST_DL_LOCATION / constants.FILENAME_HISTORY

def test_dlmediaShouldCheckAbortFlag_ForEveryUser(mock_bindings):
    users = ['abby', 'bobby', 'charlie', 'daddy']
    mock_bindings.get_users.return_value = users
    mock_abort = mock_bindings.get_abort.return_value

    dlmedia(mock_bindings)
    assert len(mock_abort.is_set.call_args_list) == len(users)

def test_dlmedaShouldNotCallDownloadMedia_whenAbortFlagIsSet(mock_bindings):
    users = ['abby', 'bobby', 'charlie', 'daddy']
    mock_bindings.get_users.return_value = users
    mock_bindings.get_abort.return_value.is_set.return_value = True
    mock_download_media = mock_bindings.download_media

    dlmedia(mock_bindings)

    assert len(mock_download_media.call_args_list) == 0

@pytest.mark.flaky
def test_dlMediaDownloads0ImagesWhenHistoryPresent(use_test_settings):
    userListFile = PROJECT_DIR / 'testdata' / 'userlists'/ 'me.txt'
    existingHistory = PROJECT_DIR / 'testdata' / 'history' / 'history_poopoopanda21.json'

    shutil.copyfile(existingHistory, TEST_DL_LOCATION / constants.FILENAME_HISTORY)
    shutil.copyfile(userListFile, TEST_DL_LOCATION / constants.FILENAME_USERS)
    bindings = RuntimeBindings(PROJECT_DIR)
    
    dlmedia(bindings)

    assert not Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZFWPUYAABM6m.jpg').exists()
    assert not Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZDQgU0AAAOgl.jpg').exists()
    assert not Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZAe4UEAAabKm.jpg').exists()

    assert Path(existingHistory).exists()

@pytest.mark.flaky
def test_dlMediaDownloads3Images(use_test_settings):
    userListFile = PROJECT_DIR / 'testdata' / 'userlists'/ 'me.txt'

    shutil.copyfile(userListFile, TEST_DL_LOCATION / constants.FILENAME_USERS)
    bindings = RuntimeBindings(PROJECT_DIR)

    dlmedia(bindings)

    assert Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZFWPUYAABM6m.jpg').exists()
    assert Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZDQgU0AAAOgl.jpg').exists()
    assert Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZAe4UEAAabKm.jpg').exists()
