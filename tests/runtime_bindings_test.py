import shutil
from unittest.mock import patch, create_autospec
from pathlib import Path

import pytest

from twitter_image_dl.runtime_bindings import RuntimeBindings
from twitter_image_dl.retrieve_twitterAPI import TweetsRetriever_TwitterAPI
from twitter_image_dl.download_history import DownloadHistory
from twitter_image_dl.settings import Settings
import twitter_image_dl.exceptions as exceptions
import twitter_image_dl.setting_strings as strings

PROJECT_DIR = Path(__file__).resolve().parents[0]

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
        ) as mock_downloadmedia \
    :
        mock_retriever.return_value = create_autospec(TweetsRetriever_TwitterAPI)
        mock_history.return_value = create_autospec(DownloadHistory)
        mock_settings.return_value = create_autospec(Settings)

        yield dict(
            readuserlist=mock_readuserlist,
            retriever=mock_retriever,
            history=mock_history,
            settings=mock_settings,
            downloadmedia=mock_downloadmedia
        )

class TestValidations:
    def test_raiseErrorWhenNoAPIOptionsAreFoundInSettings(self, tmp_path, mocks):
        mocks['settings'].return_value.get.return_value = {
            strings.APP_SECTION: {
                strings.SAVE_LOCATION: tmp_path
            },
            strings.API_SECTION: {
                strings.ACCESS_TOKEN: '',
                strings.ACCESS_SECRET: '',
                strings.CONSUMER_KEY: '',
                strings.CONSUMER_SECRET: '',
            }
        }
        
        with pytest.raises(exceptions.APINotFound) as e:
            bindings = RuntimeBindings(tmp_path)

    def test_raiseErrorWhenSaveLocationDoesNotExist(self, tmp_path, mocks):
        mocks['settings'].return_value.get.return_value = {
            strings.APP_SECTION: {
                strings.SAVE_LOCATION: Path('some', 'nonexistant', 'path')
            },
            strings.API_SECTION: {
                strings.ACCESS_TOKEN: 'some_value',
                strings.ACCESS_SECRET: 'some_value',
                strings.CONSUMER_KEY: 'some_value',
                strings.CONSUMER_SECRET: 'some_value',
            }
        }

        with pytest.raises(exceptions.SaveLocationNotExist) as e:
            bindings = RuntimeBindings(tmp_path)
