import os
import logging
from pathlib import Path

from twitter_image_dl.readUserList import readUserList
from twitter_image_dl.retrieve_twitterAPI import TweetsRetriever_TwitterAPI
from twitter_image_dl.download_history import DownloadHistory
from twitter_image_dl.settings import Settings
from twitter_image_dl.download import downloadMedia
from twitter_image_dl.dltask_scheduler import DltaskScheduler
from twitter_image_dl.abort_flag import AbortFlag
import twitter_image_dl.global_constants as constants
import twitter_image_dl.exceptions as exceptions
import twitter_image_dl.global_constants as constants

logger = logging.getLogger(__name__)

"""
Class that provides bindings to other dependant classes/functions
for twitterimagedl.py
Makes it easier to swap out classes with mocks/fakes for tests
"""
class RuntimeBindings:
    def __init__(self, app_path):
        logging.info('Initializing objects')

        self._settings = Settings(app_path / constants.FILENAME_SETTINGS)
        self._save_location = Path(
            self._settings.get()[constants.GENERAL_SECTION][constants.SAVE_LOCATION]
        )
        self._users = readUserList(self._save_location / constants.FILENAME_USERS)
        self._history = DownloadHistory()
        self._retriever = TweetsRetriever_TwitterAPI(
            self._history, self._settings
        )
        self._scheduler = DltaskScheduler(app_path)
        self._abort = AbortFlag()

        logging.info('Finished initializing objects')

    def get_settings(self):
        return self._settings

    def get_save_location(self):
        return self._save_location

    def get_users(self):
        return self._users

    def get_history(self):
        return self._history

    def get_tweet_retriever(self):
        return self._retriever

    def get_scheduler(self):
        return self._scheduler

    def get_abort(self):
        return self._abort

    def download_media(self, url, savepath):
        downloadMedia(url, savepath)
