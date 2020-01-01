from pathlib import Path
import shutil
import sys

import pytest
    
PROJECT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_DIR / 'src'
TEST_DL_LOCATION = PROJECT_DIR / 'testdata' / 'download'

sys.path.append(str( SRC_DIR ))
from twitterimagedl import dlmedia

@pytest.fixture(scope='function')
def cleanupTestDL():
    for f in TEST_DL_LOCATION.iterdir():
        if f.is_file():
            f.unlink()
        elif f.is_dir():
            shutil.rmtree(f)

sysArgs = []
@pytest.fixture(scope='function')
def restoreSysArgs():
    sysArgs = sys.argv
    yield
    sys.argv = sysArgs

def test_dirCreation(cleanupTestDL, restoreSysArgs):
    userListFile = str(PROJECT_DIR / 'testdata' / 'userlists'/ 'me.txt')
    saveLocation = str(TEST_DL_LOCATION)
    existingHistory = str(PROJECT_DIR / 'testdata' / 'history' / 'history_poopoopanda21.json')
    sys.argv = [sys.argv[0], userListFile, saveLocation, existingHistory]

    dlmedia()

    assert Path(saveLocation, 'poopoopanda21').exists()
    assert Path(saveLocation, 'poopoopanda21', 'images').exists()
    assert Path(saveLocation, 'poopoopanda21', 'gifs').exists()
    assert Path(saveLocation, 'poopoopanda21', 'videos').exists()

def test_dlMediaDownloads0ImagesWhenHistoryPresent(cleanupTestDL, restoreSysArgs):
    userListFile = str(PROJECT_DIR / 'testdata' / 'userlists'/ 'me.txt')
    saveLocation = str(TEST_DL_LOCATION)
    existingHistory = str(PROJECT_DIR / 'testdata' / 'history' / 'history_poopoopanda21.json')
    sys.argv = [sys.argv[0], userListFile, saveLocation, existingHistory]

    dlmedia()

    assert not Path(saveLocation, 'poopoopanda21', 'images', 'EGWZFWPUYAABM6m.jpg').exists()
    assert not Path(saveLocation, 'poopoopanda21', 'images', 'EGWZDQgU0AAAOgl.jpg').exists()
    assert not Path(saveLocation, 'poopoopanda21', 'images', 'EGWZAe4UEAAabKm.jpg').exists()

    assert Path(existingHistory).exists()

def test_dlMediaDownloads3Images(cleanupTestDL, restoreSysArgs):
    userListFile = str(PROJECT_DIR / 'testdata' / 'userlists'/ 'me.txt')
    saveLocation = str(TEST_DL_LOCATION)
    nonExistantHistory = str(TEST_DL_LOCATION / 'history.txt')
    sys.argv = [sys.argv[0], userListFile, saveLocation, nonExistantHistory]

    dlmedia()

    assert Path(saveLocation, 'poopoopanda21', 'images', 'EGWZFWPUYAABM6m.jpg').exists()
    assert Path(saveLocation, 'poopoopanda21', 'images', 'EGWZDQgU0AAAOgl.jpg').exists()
    assert Path(saveLocation, 'poopoopanda21', 'images', 'EGWZAe4UEAAabKm.jpg').exists()

    assert Path(nonExistantHistory).exists()