from pathlib import Path
from configparser import ConfigParser
from copy import deepcopy

import twitter_image_dl.global_constants as constants
import twitter_image_dl.exceptions as exceptions
from twitter_image_dl.dltask_scheduler import DltaskScheduler

# helpers

def must_be_number_between(min, max):
    # min max is inclusive
    def validator(value):
        if not value.isnumeric():
            return False

        return min <= int(value) <= max

    return validator

def must_be_number_in(allowed_values):
    def validator(value):
        if not value.isnumeric():
            return False

        return int(value) in allowed_values

    return validator

def string_to_bool_converter(string):
    return bool( int(string) )

def bool_to_string_converter(bool):
    return '1' if bool else '0'

def schedule_to_string(schedule):
    return str(schedule.value)

def string_to_schedule(string):
    return DltaskScheduler.ScheduleOptions(int(string))

schedule_values = [
    member.value for member in DltaskScheduler.ScheduleOptions.__members__.values()
] # convert schedule enums to underlying integer values

class Settings:
    # functions to validate values read from settings file
    OPTION_VALIDATORS = {
        constants.SAVE_LOCATION: lambda value: value != '',
        constants.IS_SCHEDULED: must_be_number_between(0, 1),
        constants.SCHEDULE_PERIOD: must_be_number_in(schedule_values),
        constants.START_HOUR: must_be_number_between(0, 23),
        constants.START_MINUTE: must_be_number_between(0, 59),
    }
    # conversion functions for data coming in/out of this class
    OPTION_CONVERTERS = {
        constants.SAVE_LOCATION: { 'set': str, 'get': Path },
        constants.IS_SCHEDULED: { 'set': bool_to_string_converter, 'get': string_to_bool_converter },
        constants.SCHEDULE_PERIOD: { 'set': schedule_to_string, 'get': string_to_schedule },
        constants.START_HOUR: { 'set': str, 'get': int },
        constants.START_MINUTE: { 'set': str, 'get': int },
    }

    def __init__(self, filepath):
        self._filepath = filepath
        self._parser = ConfigParser()
        self._settings = {}

        self._configureParser()
        self._readSettingsFromFile()
        self._normalizeSettings()
    
    def get(self):
        settings = deepcopy(self._settings)
        
        # convert to types meaningful to rest of the app
        for section, options in settings.items():
            for name, option in options.items():
                convert = self._get_option_converter(name, 'get')
                settings[section][name] = convert(option)

        return settings

    def set(self, settings):
        copy = deepcopy(settings)
        for section, options in copy.items():
            self._settings[section].update(options)

            # convert to storeable values
            for name, option in options.items():
                convert = self._get_option_converter(name, 'set')
                self._settings[section][name] = convert(option)
        
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
            raise exceptions.APINotFound('Please make sure to fill out Twitter API related options in settings')
        if (
            not Path(self._settings[constants.GENERAL_SECTION][constants.SAVE_LOCATION]).exists()
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
        self._create_missing_sections()
        self._convert_invalid_values()

    def _create_missing_sections(self):
        if constants.API_SECTION not in self._settings:
            options = [
                constants.ACCESS_TOKEN,
                constants.ACCESS_SECRET,
                constants.CONSUMER_KEY,
                constants.CONSUMER_SECRET,
            ]
            self._set_default_section(constants.API_SECTION, options)
        
        if constants.GENERAL_SECTION not in self._settings:
            options = [constants.SAVE_LOCATION]
            self._set_default_section(constants.GENERAL_SECTION, options)

        if constants.SCHEDULE_SECTION not in self._settings:
            options = [
                constants.IS_SCHEDULED,
                constants.SCHEDULE_PERIOD,
                constants.START_HOUR,
                constants.START_MINUTE,
            ]
            self._set_default_section(constants.SCHEDULE_SECTION, options)

    def _convert_invalid_values(self):
        section = constants.GENERAL_SECTION
        options = [constants.SAVE_LOCATION]
        self._convert_section_invalid_values(section, options)

        section = constants.SCHEDULE_SECTION
        options = [
            constants.IS_SCHEDULED,
            constants.SCHEDULE_PERIOD,
            constants.START_HOUR,
            constants.START_MINUTE,
        ]
        self._convert_section_invalid_values(section, options)

    def _set_default_section(self, section, options):
        self._settings[section] = {
            option: self._get_default(option) for option in options
        }

    def _convert_section_invalid_values(self, section, options):
        for option in options:
            validator = self._get_option_validator(option)
            if not validator( self._settings[section][option] ):
                self._settings[section][option] = self._get_default(option)

    def _get_default(self, option):
        DEFAULT_VALUE_GETTER = {
            constants.SAVE_LOCATION: str(self._filepath.parents[0]),
            constants.IS_SCHEDULED: '0',
            constants.SCHEDULE_PERIOD: '0',
            constants.START_HOUR: '0',
            constants.START_MINUTE: '0',
        }

        return DEFAULT_VALUE_GETTER.get(option, '')

    def _get_option_validator(self, option):
        return self.OPTION_VALIDATORS.get(option, lambda value: True)

    def _get_option_converter(self, option, get_or_set):
        converters = self.OPTION_CONVERTERS.get(option, None)
        if not converters:
            return lambda value: value
        else:
            return converters[get_or_set]
