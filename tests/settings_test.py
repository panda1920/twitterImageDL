from pathlib import Path
import sys
import shutil

import pytest

import twitter_image_dl.global_constants as constants
import twitter_image_dl.exceptions as exceptions
from twitter_image_dl.settings import Settings

PROJECT_DIR = Path(__file__).resolve().parents[1]
TEST_DATA_DIR = PROJECT_DIR / 'testdata' / 'settings'
TEST_SETTINGS_FILE = TEST_DATA_DIR / 'settings.txt'
SAMPLE_SETTINGS_FILE = TEST_DATA_DIR / 'sample_settings.txt'

@pytest.fixture(scope='function', autouse=True)
def clearTestData():
    yield
    
    if TEST_SETTINGS_FILE.exists():
        TEST_SETTINGS_FILE.unlink()

class Test_readSettings:
    def test_shouldReadValueFromGoodSettingFile(self):
        settings = Settings(SAMPLE_SETTINGS_FILE).get()

        assert settings[constants.GENERAL_SECTION]['save_location'] == Path(r'C:\Users\user1\dir1\dir\dir3')

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == 'test_access_token'
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == 'test_access_secret'
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == 'test_consumer_key'
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == 'test_consumer_secret'

        assert settings[constants.SCHEDULE_SECTION][constants.IS_SCHEDULED] == 1
        assert settings[constants.SCHEDULE_SECTION][constants.SCHEDULE_PERIOD] == 1
        assert settings[constants.SCHEDULE_SECTION][constants.START_HOUR] == 1
        assert settings[constants.SCHEDULE_SECTION][constants.START_MINUTE] == 1

    def test_shouldStripWhitespace_AfterParsing(self):
        space_settings_file = TEST_DATA_DIR / 'settings_spaces.txt'

        settings = Settings(space_settings_file).get()

        assert settings[constants.GENERAL_SECTION]['save_location'] == Path(r'C:\Users\user1\dir1\dir\dir3')

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == 'test_access_token'
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == 'test_access_secret'
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == 'test_consumer_key'
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == 'test_consumer_secret'

        assert settings[constants.SCHEDULE_SECTION][constants.IS_SCHEDULED] == 1
        assert settings[constants.SCHEDULE_SECTION][constants.SCHEDULE_PERIOD] == 1
        assert settings[constants.SCHEDULE_SECTION][constants.START_HOUR] == 1
        assert settings[constants.SCHEDULE_SECTION][constants.START_MINUTE] == 1

    def test_shouldInsertEmptyStringeAsDefaultValue_ForNonExistingSection(self):
        no_api_section = TEST_DATA_DIR / 'no_twitter_api.txt'
        
        settings = Settings(no_api_section).get()

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == ''
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == ''

    def test_shouldGenerateFilePathDirAsDefaultValue_ForNonExistingGeneralSection(self):
        no_general_section = TEST_DATA_DIR / 'no_general_settings.txt'
        file_location = no_general_section.parents[0]

        settings = Settings(no_general_section).get()

        assert settings[constants.GENERAL_SECTION][constants.SAVE_LOCATION] == file_location

    def test_shouldGenerateDefaultValue_ForNonExistingScheduleSection(self):
        no_schedule_section = TEST_DATA_DIR / 'no_schedule_settings.txt'
        file_location = no_schedule_section.parents[0]

        settings = Settings(no_schedule_section).get()

        assert settings[constants.SCHEDULE_SECTION][constants.IS_SCHEDULED] == 0
        assert settings[constants.SCHEDULE_SECTION][constants.SCHEDULE_PERIOD] == 1
        assert settings[constants.SCHEDULE_SECTION][constants.START_HOUR] == 0
        assert settings[constants.SCHEDULE_SECTION][constants.START_MINUTE] == 0

    def test_shouldGenerateDefaultValues_whenFileNonExistant(self):
        nonexistant_file = TEST_DATA_DIR / '123120381028309128309123.txt'
        file_location = nonexistant_file.parents[0]

        settings = Settings(nonexistant_file).get()

        assert settings[constants.GENERAL_SECTION][constants.SAVE_LOCATION] == file_location

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == ''
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == ''

        assert settings[constants.SCHEDULE_SECTION][constants.IS_SCHEDULED] == 0
        assert settings[constants.SCHEDULE_SECTION][constants.SCHEDULE_PERIOD] == 1
        assert settings[constants.SCHEDULE_SECTION][constants.START_HOUR] == 0
        assert settings[constants.SCHEDULE_SECTION][constants.START_MINUTE] == 0

    def test_shouldGenerateEmptyString_whenOptionsAreEmpty(self):
        empty_file = TEST_DATA_DIR / 'empty.txt'
        file_location = empty_file.parents[0]

        settings = Settings(empty_file).get()

        assert settings[constants.GENERAL_SECTION][constants.SAVE_LOCATION] == file_location

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == ''
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == ''

        assert settings[constants.SCHEDULE_SECTION][constants.IS_SCHEDULED] == 0
        assert settings[constants.SCHEDULE_SECTION][constants.SCHEDULE_PERIOD] == 1
        assert settings[constants.SCHEDULE_SECTION][constants.START_HOUR] == 0
        assert settings[constants.SCHEDULE_SECTION][constants.START_MINUTE] == 0

class Test_writeSettings:
    def test_setShouldReplaceSettingState(self):
        new_settings = {
            constants.GENERAL_SECTION: {
                constants.SAVE_LOCATION: Path('new'),
            },
            constants.API_SECTION: {
                constants.ACCESS_TOKEN: 'new',
                constants.ACCESS_SECRET: 'new',
                constants.CONSUMER_KEY: 'new',
                constants.CONSUMER_SECRET: 'new',
            },
        }
        general_settings = Settings(SAMPLE_SETTINGS_FILE)

        general_settings.set(new_settings)
        
        settings = general_settings.get()
        for section_name, section in new_settings.items():
            for option_name, option in section.items():
                assert settings[section_name][option_name] == option

    def test_writeShouldWriteValueToSettingsFile(self):
        shutil.copyfile(SAMPLE_SETTINGS_FILE, TEST_SETTINGS_FILE)
        general_settings = Settings(TEST_SETTINGS_FILE)
        new_settings = {
            constants.GENERAL_SECTION: {
                constants.SAVE_LOCATION: Path('new'),
            },
            constants.API_SECTION: {
                constants.ACCESS_TOKEN: 'new',
                constants.ACCESS_SECRET: 'new',
                constants.CONSUMER_KEY: 'new',
                constants.CONSUMER_SECRET: 'new',
            },
        }

        general_settings.set(new_settings)
        general_settings.write()

        settings = Settings(TEST_SETTINGS_FILE).get()
        for section_name, section in new_settings.items():
            for option_name, option in section.items():
                assert settings[section_name][option_name] == option

    def test_writeShouldWriteValueToNonExistantSettingsFile(self):
        assert TEST_SETTINGS_FILE.exists() == False

        general_settings = Settings(TEST_SETTINGS_FILE)
        sample_settings = Settings(SAMPLE_SETTINGS_FILE).get()

        general_settings.set(sample_settings)
        general_settings.write()

        assert TEST_SETTINGS_FILE.exists() == True
        settings = Settings(TEST_SETTINGS_FILE).get()
        for section_name, section in sample_settings.items():
            for option_name, option in section.items():
                assert settings[section_name][option_name] == option

class TestValidation:
    def test_raiseErrorWhenNoAPIOptionsAreFoundInSettings(self):
        empty_file = TEST_DATA_DIR / 'empty.txt'
        general_settings = Settings(empty_file)

        with pytest.raises(exceptions.APINotFound) as e:
            general_settings.validate_settings()

    def test_raiseErrorWhenSaveLocationDoesNotExist(self):
        general_settings = Settings(SAMPLE_SETTINGS_FILE)

        with pytest.raises(exceptions.SaveLocationNotExist) as e:
            general_settings.validate_settings()
