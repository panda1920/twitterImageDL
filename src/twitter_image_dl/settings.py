from configparser import ConfigParser

import twitter_image_dl.setting_strings as strings

class Settings:
    def __init__(self, filepath):
        self._filepath = filepath
        self._parser = ConfigParser()
        self._settings = {}

        self._configureParser()
        self._readSettingsFromFile()
        self._normalizeSettings()
    
    def get(self):
        return { **self._settings }

    def set(self, settings):
        self._settings = settings

    def write(self):
        self._parser.read_dict(self._settings)
        with self._filepath.open(mode='w', encoding='utf-8') as fp:
            self._parser.write(fp)

    def _configureParser(self):
        # avoid automatic conversion of each option names to lower case
        self._parser.optionxform = lambda option: option

    def _readSettingsFromFile(self):
        self._parser.read(self._filepath)
        for section, items in self._parser.items():
            self._settings[section] = { k: items[k] for k in items }

    def _normalizeSettings(self):
        if strings.API_SECTION not in self._settings:
            self._settings[strings.API_SECTION] = {
                strings.ACCESS_TOKEN: self._get_default(strings.ACCESS_TOKEN),
                strings.ACCESS_SECRET: self._get_default(strings.ACCESS_SECRET),
                strings.CONSUMER_TOKEN: self._get_default(strings.CONSUMER_TOKEN),
                strings.CONSUMER_SECRET: self._get_default(strings.CONSUMER_SECRET),
            }
        
        if strings.APP_SECTION not in self._settings:
            self._settings[strings.APP_SECTION] = {
                strings.SAVE_LOCATION: self._get_default(strings.SAVE_LOCATION)
            }
        
        if self._settings[strings.APP_SECTION][strings.SAVE_LOCATION] == '':
            self._settings[strings.APP_SECTION][strings.SAVE_LOCATION] = self._get_default(strings.SAVE_LOCATION)

    def _get_default(self, option):
        default_value_getter = {
            strings.SAVE_LOCATION: self._filepath.parents[0],
        }

        return default_value_getter.get(option, '')
