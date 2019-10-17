from pathlib import Path
import shutil
import sys
import os.path

import pytest
    
PROJECT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_DIR / 'src'
TEST_DL_LOCATION = PROJECT_DIR / 'testdata' / 'download'

sys.path.append(str( SRC_DIR ))

import exceptions
from twitterimagedl import dlimage

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

def test_dlImageDownloads3Images(cleanupTestDL, restoreSysArgs):
    userListFile = str(PROJECT_DIR / 'testdata' / 'userlists'/ 'me.txt')
    saveLocation = str(TEST_DL_LOCATION)
    sys.argv = [sys.argv[0], userListFile, saveLocation]

    dlimage()

    assert Path(saveLocation, 'poopoopanda21', 'EGWZFWPUYAABM6m.jpg').exists()
    assert Path(saveLocation, 'poopoopanda21', 'EGWZDQgU0AAAOgl.jpg').exists()
    assert Path(saveLocation, 'poopoopanda21', 'EGWZAe4UEAAabKm.jpg').exists()