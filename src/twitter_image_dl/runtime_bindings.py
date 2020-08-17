import os
from pathlib import Path

from twitter_image_dl.readUserList import readUserList
from twitter_image_dl.retrieve_twitterAPI import TweetsRetriever_TwitterAPI
from twitter_image_dl.download_history import DownloadHistory
from twitter_image_dl.settings import Settings
from twitter_image_dl.download import downloadMedia
from twitter_image_dl.dltask_scheduler import DltaskScheduler
import twitter_image_dl.global_constants as constants
import twitter_image_dl.exceptions as exceptions
import twitter_image_dl.global_constants as constants

"""
Class that provides bindings to other dependant classes/functions
for twitterimagedl.py
Makes it easier to swap out classes with mocks/fakes for tests
"""
class RuntimeBindings:
    def __init__(self, app_path):
        self._settings = Settings(app_path / constants.FILENAME_SETTINGS)
        self._validateSettings()
        self._save_location = Path(
            self._settings.get()[constants.APP_SECTION][constants.SAVE_LOCATION]
        )
        self._users = readUserList(self._save_location / constants.FILENAME_USERS)
        self._history = DownloadHistory(
            self._save_location / constants.FILENAME_HISTORY
        )
        self._retriever = TweetsRetriever_TwitterAPI(
            self._history, self._settings
        )
        self._scheduler = DltaskScheduler(app_path)

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

    def download_media(self, url, savepath):
        downloadMedia(url, savepath)
        
    def _validateSettings(self):
        app_settings = self._settings.get()
        if (
            app_settings[constants.API_SECTION][constants.ACCESS_TOKEN] == '' or
            app_settings[constants.API_SECTION][constants.ACCESS_SECRET] == '' or
            app_settings[constants.API_SECTION][constants.CONSUMER_KEY] == '' or
            app_settings[constants.API_SECTION][constants.CONSUMER_SECRET] == ''
        ):
            raise exceptions.APINotFound('Please make sure to fill out twitter API related options in settings')
        if (
            not Path(app_settings[constants.APP_SECTION][constants.SAVE_LOCATION]).exists()
        ):
            raise exceptions.SaveLocationNotExist('Please make sure to specify a valid save location in settings')
