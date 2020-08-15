from pathlib import Path
import shutil
import sys

import pytest
    
from twitter_image_dl.twitterimagedl import dlmedia
from twitter_image_dl.runtime_bindings import RuntimeBindings
import twitter_image_dl.exceptions as exceptions

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

@pytest.fixture(scope='function', autouse=True)
def use_test_settings():
    test_settings = PROJECT_DIR / 'testdata' / 'settings' / 'settings.conf'
    copied_settings = PROJECT_DIR / 'settings.conf'
    shutil.copyfile(test_settings, copied_settings)

    yield

    copied_settings.unlink()

def test_dlMediaDownloads0ImagesWhenHistoryPresent():
    userListFile = PROJECT_DIR / 'testdata' / 'userlists'/ 'me.txt'
    existingHistory = PROJECT_DIR / 'testdata' / 'history' / 'history_poopoopanda21.json'

    shutil.copyfile(existingHistory, TEST_DL_LOCATION / 'history.json')
    shutil.copyfile(userListFile, TEST_DL_LOCATION / 'users.txt')
    bindings = RuntimeBindings(PROJECT_DIR)
    
    dlmedia(bindings)

    assert not Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZFWPUYAABM6m.jpg').exists()
    assert not Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZDQgU0AAAOgl.jpg').exists()
    assert not Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZAe4UEAAabKm.jpg').exists()

    assert Path(existingHistory).exists()

def test_dlMediaDownloads3Images():
    userListFile = PROJECT_DIR / 'testdata' / 'userlists'/ 'me.txt'

    shutil.copyfile(userListFile, TEST_DL_LOCATION / 'users.txt')
    bindings = RuntimeBindings(PROJECT_DIR)

    dlmedia(bindings)

    assert Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZFWPUYAABM6m.jpg').exists()
    assert Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZDQgU0AAAOgl.jpg').exists()
    assert Path(TEST_DL_LOCATION, 'poopoopanda21', 'images', 'EGWZAe4UEAAabKm.jpg').exists()

# def test_dlmedia_raiseErrorWhenNoAPIOptionsAreFoundInSettings():
#     test_settings = PROJECT_DIR / 'testdata' / 'settings' / 'empty.txt'
#     shutil.copy(test_settings, PROJECT_DIR / 'settings.conf')
#     bindings = RuntimeBindings(PROJECT_DIR)
    
#     with pytest.raises(exceptions.APINotFound) as e:
#         dlmedia(bindings)

#     try:
#         (PROJECT_DIR / 'history.json').unlink()
#         (PROJECT_DIR / 'users.txt').unlink()
#     except:
#         pass

# def test_dlmedia_raiseErrorWhenSaveLocationDoesNotExist():
#     test_settings = PROJECT_DIR / 'testdata' / 'settings' / 'good_settings.txt'
#     shutil.copy(test_settings, PROJECT_DIR / 'settings.conf')
#     bindings = RuntimeBindings(PROJECT_DIR)

#     with pytest.raises(exceptions.SaveLocationNotExist) as e:
#         dlmedia(bindings)
