import shutil
from unittest.mock import patch, create_autospec
from pathlib import Path

import pytest

from twitter_image_dl.runtime_bindings import RuntimeBindings
from twitter_image_dl.retrieve_twitterAPI import TweetsRetriever_TwitterAPI
from twitter_image_dl.download_history import DownloadHistory
from twitter_image_dl.dltask_scheduler import DltaskScheduler
from twitter_image_dl.settings import Settings
import twitter_image_dl.exceptions as exceptions
import twitter_image_dl.global_constants as constants
import twitter_image_dl.global_constants as constants

PROJECT_DIR = Path(__file__).resolve().parents[1]
DOWNLOAD_DIR = PROJECT_DIR / 'testdata' / 'download'

@pytest.fixture(scope='function')
def mocks():
    with \
        patch(
            'twitter_image_dl.runtime_bindings.readUserList'
        ) as mock_readuserlist, \
        patch(
            'twitter_image_dl.runtime_bindings.TweetsRetriever_TwitterAPI',
            autospec=True
        ) as mock_retriever, \
        patch(
            'twitter_image_dl.runtime_bindings.DownloadHistory',
            autospec=True
        ) as mock_history, \
        patch(
            'twitter_image_dl.runtime_bindings.Settings',
            autospec=True
        ) as mock_settings, \
        patch(
            'twitter_image_dl.runtime_bindings.downloadMedia'
        ) as mock_downloadmedia, \
        patch(
            'twitter_image_dl.runtime_bindings.DltaskScheduler',
            autospec=True
        ) as mock_scheduler \
    :
        mock_retriever.return_value = create_autospec(TweetsRetriever_TwitterAPI)
        mock_history.return_value = create_autospec(DownloadHistory)
        mock_scheduler.return_value = create_autospec(DltaskScheduler)
        implement_mock_settings(mock_settings)

        yield dict(
            readuserlist=mock_readuserlist,
            retriever=mock_retriever,
            history=mock_history,
            settings=mock_settings,
            downloadmedia=mock_downloadmedia,
            scheduler=mock_scheduler,
        )

@pytest.fixture(scope='function', autouse=True)
def clear_download_dir():
    yield
    shutil.rmtree(DOWNLOAD_DIR)
    DOWNLOAD_DIR.mkdir()

def implement_mock_settings(mock_settings):
    mock_settings.return_value = create_autospec(Settings)

    mock_settings.return_value.get.return_value = {
        constants.APP_SECTION: {
            constants.SAVE_LOCATION: DOWNLOAD_DIR
        },
        constants.API_SECTION: {
            constants.ACCESS_TOKEN: 'some_value',
            constants.ACCESS_SECRET: 'some_value',
            constants.CONSUMER_KEY: 'some_value',
            constants.CONSUMER_SECRET: 'some_value',
        }
    }

class TestValidations:
    def test_raiseErrorWhenNoAPIOptionsAreFoundInSettings(self, tmp_path, mocks):
        mocks['settings'].return_value.get.return_value = {
            constants.APP_SECTION: {
                constants.SAVE_LOCATION: tmp_path
            },
            constants.API_SECTION: {
                constants.ACCESS_TOKEN: '',
                constants.ACCESS_SECRET: '',
                constants.CONSUMER_KEY: '',
                constants.CONSUMER_SECRET: '',
            }
        }
        
        with pytest.raises(exceptions.APINotFound) as e:
            bindings = RuntimeBindings(tmp_path)

    def test_raiseErrorWhenSaveLocationDoesNotExist(self, tmp_path, mocks):
        mocks['settings'].return_value.get.return_value = {
            constants.APP_SECTION: {
                constants.SAVE_LOCATION: Path('some', 'nonexistant', 'path')
            },
            constants.API_SECTION: {
                constants.ACCESS_TOKEN: 'some_value',
                constants.ACCESS_SECRET: 'some_value',
                constants.CONSUMER_KEY: 'some_value',
                constants.CONSUMER_SECRET: 'some_value',
            }
        }

        with pytest.raises(exceptions.SaveLocationNotExist) as e:
            bindings = RuntimeBindings(tmp_path)

class TestInstantiation:
    def test_instantiatedSettingIsPassedAppPath(self, tmp_path, mocks):
        bindings = RuntimeBindings(tmp_path)

        assert len(mocks['settings'].call_args_list) == 1
        path, *_ = mocks['settings'].call_args_list[0][0]
        assert path == tmp_path / constants.FILENAME_SETTINGS

    def test_pathPassedToReadUserListIsSaveLocationInSetting(self, tmp_path, mocks):
        bindings = RuntimeBindings(tmp_path)
        settings = mocks['settings'](DOWNLOAD_DIR).get()
        save_location = settings[constants.APP_SECTION][constants.SAVE_LOCATION]

        assert len(mocks['readuserlist'].call_args_list) == 1
        path, *_ = mocks['readuserlist'].call_args_list[0][0]
        assert path == save_location / constants.FILENAME_USERS

    def test_pathPassedToHistoryIsSaveLocationInSetting(self, tmp_path, mocks):
        bindings = RuntimeBindings(tmp_path)
        settings = mocks['settings'](DOWNLOAD_DIR).get()
        save_location = settings[constants.APP_SECTION][constants.SAVE_LOCATION]

        assert len(mocks['history'].call_args_list) == 1
        path, *_ = mocks['history'].call_args_list[0][0]
        assert path == save_location / constants.FILENAME_HISTORY

    def test_instantiatedSettingAndHistoryIsPassedToRetriever(self, tmp_path, mocks):
        bindings = RuntimeBindings(tmp_path)
        settings = mocks['settings'].return_value
        history = mocks['history'].return_value

        assert len(mocks['retriever'].call_args_list) == 1
        passed_history, passed_settings, *_ = mocks['retriever'].call_args_list[0][0]
        assert passed_history == history
        assert passed_settings == settings

    def test_instantiatedSchedulerIsPassedAppPath(self, tmp_path, mocks):
        bindings = RuntimeBindings(tmp_path)
        mock_scheduler = mocks['scheduler']

        assert len(mock_scheduler.call_args_list) == 1
        path, *_ = mock_scheduler.call_args_list[0][0]
        assert path == tmp_path
