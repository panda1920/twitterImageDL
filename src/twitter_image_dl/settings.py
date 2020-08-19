from pathlib import Path
from configparser import ConfigParser
from copy import deepcopy

import twitter_image_dl.global_constants as constants
import twitter_image_dl.exceptions as exceptions

class Settings:
    def __init__(self, filepath):
        self._filepath = filepath
        self._parser = ConfigParser()
        self._settings = {}

        self._configureParser()
        self._readSettingsFromFile()
        self._normalizeSettings()
    
    def get(self):
        settings = deepcopy(self._settings)
        # convert to Path object when presenting to outside world
        settings[constants.APP_SECTION][constants.SAVE_LOCATION] = Path( settings[constants.APP_SECTION][constants.SAVE_LOCATION] )

        return settings

    def set(self, settings):
        self._settings = deepcopy(settings)
        # store as normal string
        self._settings[constants.APP_SECTION][constants.SAVE_LOCATION] = str( self._settings[constants.APP_SECTION][constants.SAVE_LOCATION] )

    def write(self):
        self._parser.read_dict(self._settings)
        with self._filepath.open(mode='w', encoding='utf-8') as fp:
            self._parser.write(fp)

    def validate_settings(self):
        if (
            self._settings[constants.API_SECTION][constants.ACCESS_TOKEN] == '' or
            self._settings[constants.API_SECTION][constants.ACCESS_SECRET] == '' or
            self._settings[constants.API_SECTION][constants.CONSUMER_KEY] == '' or
            self._settings[constants.API_SECTION][constants.CONSUMER_SECRET] == ''
        ):
            raise exceptions.APINotFound('Please make sure to fill out twitter API related options in settings')
        if (
            not Path(self._settings[constants.APP_SECTION][constants.SAVE_LOCATION]).exists()
        ):
            raise exceptions.SaveLocationNotExist('Please make sure to specify a valid save location in settings')

    def _configureParser(self):
        # avoid automatic conversion of each option names to lower case
        self._parser.optionxform = lambda option: option

    def _readSettingsFromFile(self):
        self._parser.read(self._filepath)
        for section, items in self._parser.items():
            self._settings[section] = { k: items[k] for k in items }

    def _normalizeSettings(self):
        if constants.API_SECTION not in self._settings:
            self._settings[constants.API_SECTION] = {
                constants.ACCESS_TOKEN: self._get_default(constants.ACCESS_TOKEN),
                constants.ACCESS_SECRET: self._get_default(constants.ACCESS_SECRET),
                constants.CONSUMER_KEY: self._get_default(constants.CONSUMER_KEY),
                constants.CONSUMER_SECRET: self._get_default(constants.CONSUMER_SECRET),
            }
        
        if constants.APP_SECTION not in self._settings:
            self._settings[constants.APP_SECTION] = {
                constants.SAVE_LOCATION: self._get_default(constants.SAVE_LOCATION)
            }
        
        if self._settings[constants.APP_SECTION][constants.SAVE_LOCATION] == '':
            self._settings[constants.APP_SECTION][constants.SAVE_LOCATION] = self._get_default(constants.SAVE_LOCATION)

    def _get_default(self, option):
        default_value_getter = {
            constants.SAVE_LOCATION: str(self._filepath.parents[0]),
        }

        return default_value_getter.get(option, '')
