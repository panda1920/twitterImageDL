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

        assert settings[constants.APP_SECTION]['save_location'] == Path(r'C:\Users\user1\dir1\dir\dir3')

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == 'test_access_token'
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == 'test_access_secret'
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == 'test_consumer_key'
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == 'test_consumer_secret'

    def test_shouldStripWhitespace_AfterParsing(self):
        space_settings_file = TEST_DATA_DIR / 'settings_spaces.txt'

        settings = Settings(space_settings_file).get()

        assert settings[constants.APP_SECTION]['save_location'] == Path(r'C:\Users\user1\dir1\dir\dir3')

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == 'test_access_token'
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == 'test_access_secret'
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == 'test_consumer_key'
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == 'test_consumer_secret'

    def test_shouldInsertEmptyStringeAsDefaultValue_ForNonExistingSection(self):
        no_api_section = TEST_DATA_DIR / 'no_twitter_api.txt'
        
        settings = Settings(no_api_section).get()

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == ''
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == ''

    def test_shouldGenerateFilePathDirAsDefaultValue_ForNonExistingAppSection(self):
        no_app_section = TEST_DATA_DIR / 'no_app_settings.txt'
        file_location = no_app_section.parents[0]

        settings = Settings(no_app_section).get()

        assert settings[constants.APP_SECTION][constants.SAVE_LOCATION] == file_location

    def test_shouldGenerateDefaultValues_whenFileNonExistant(self):
        nonexistant_file = TEST_DATA_DIR / '123120381028309128309123.txt'
        file_location = nonexistant_file.parents[0]

        settings = Settings(nonexistant_file).get()

        assert settings[constants.APP_SECTION][constants.SAVE_LOCATION] == file_location

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == ''
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == ''

    def test_shouldGenerateEmptyString_whenOptionsAreEmpty(self):
        empty_file = TEST_DATA_DIR / 'empty.txt'
        file_location = empty_file.parents[0]

        settings = Settings(empty_file).get()

        assert settings[constants.APP_SECTION][constants.SAVE_LOCATION] == file_location

        assert settings[constants.API_SECTION][constants.ACCESS_TOKEN] == ''
        assert settings[constants.API_SECTION][constants.ACCESS_SECRET] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_KEY] == ''
        assert settings[constants.API_SECTION][constants.CONSUMER_SECRET] == ''

class Test_writeSettings:
    def test_setShouldReplaceSettingState(self):
        new_settings = {
            constants.APP_SECTION: {
                constants.SAVE_LOCATION: Path('new'),
            },
            constants.API_SECTION: {
                constants.ACCESS_TOKEN: 'new',
                constants.ACCESS_SECRET: 'new',
                constants.CONSUMER_KEY: 'new',
                constants.CONSUMER_SECRET: 'new',
            },
        }
        app_settings = Settings(SAMPLE_SETTINGS_FILE)

        app_settings.set(new_settings)
        
        settings = app_settings.get()
        for section_name, section in new_settings.items():
            for option_name, option in section.items():
                assert settings[section_name][option_name] == option

    def test_writeShouldWriteValueToSettingsFile(self):
        shutil.copyfile(SAMPLE_SETTINGS_FILE, TEST_SETTINGS_FILE)
        app_settings = Settings(TEST_SETTINGS_FILE)
        new_settings = {
            constants.APP_SECTION: {
                constants.SAVE_LOCATION: Path('new'),
            },
            constants.API_SECTION: {
                constants.ACCESS_TOKEN: 'new',
                constants.ACCESS_SECRET: 'new',
                constants.CONSUMER_KEY: 'new',
                constants.CONSUMER_SECRET: 'new',
            },
        }

        app_settings.set(new_settings)
        app_settings.write()

        settings = Settings(TEST_SETTINGS_FILE).get()
        for section_name, section in new_settings.items():
            for option_name, option in section.items():
                assert settings[section_name][option_name] == option

    def test_writeShouldWriteValueToNonExistantSettingsFile(self):
        assert TEST_SETTINGS_FILE.exists() == False

        app_settings = Settings(TEST_SETTINGS_FILE)
        sample_settings = Settings(SAMPLE_SETTINGS_FILE).get()

        app_settings.set(sample_settings)
        app_settings.write()

        assert TEST_SETTINGS_FILE.exists() == True
        settings = Settings(TEST_SETTINGS_FILE).get()
        for section_name, section in sample_settings.items():
            for option_name, option in section.items():
                assert settings[section_name][option_name] == option

class TestValidation:
    def test_raiseErrorWhenNoAPIOptionsAreFoundInSettings(self):
        empty_file = TEST_DATA_DIR / 'empty.txt'
        app_settings = Settings(empty_file)

        with pytest.raises(exceptions.APINotFound) as e:
            app_settings.validate_settings()

    def test_raiseErrorWhenSaveLocationDoesNotExist(self):
        app_settings = Settings(SAMPLE_SETTINGS_FILE)

        with pytest.raises(exceptions.SaveLocationNotExist) as e:
            app_settings.validate_settings()
