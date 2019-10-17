from pathlib import Path
import shutil
import sys

import pytest
    
PROJECT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_DIR / 'src'
TESTDATA_DIR = PROJECT_DIR / 'testdata'

sys.path.append(str( SRC_DIR ))

import exceptions
from parseArgument import parseArgument

sysArgs = []

@pytest.fixture(scope='function')
def restoreSysArgs():
    sysArgs = sys.argv
    yield
    sys.argv = sysArgs

def test_parseArgumentReturnsObjectWhenArgCountBT2():
    arg1 = str( TESTDATA_DIR / 'userlists' / 'list1.txt' )
    arg2 = str( TESTDATA_DIR / 'download' )
    sys.argv = [sys.argv[0], arg1, arg2]

    settings = parseArgument()
    assert 'usersListPath' in settings
    assert 'saveLocation' in settings
    assert settings['usersListPath'] == arg1
    assert settings['saveLocation'] == arg2

def test_parseArgumentThrowsWhenArgCountIsOne():
    arg1 = str( TESTDATA_DIR / 'userlists' / 'list1.txt' )
    sys.argv = [sys.argv[0], arg1]

    with pytest.raises(exceptions.InvalidArgumentCountException):
        settings = parseArgument()

def test_parseArgumentThrowsWhenArg1DoesNotExist():
    arg1 = str( TESTDATA_DIR / 'nonexistant' / 'file.txt' )
    arg2 = str( TESTDATA_DIR / 'download' )
    sys.argv = [sys.argv[0], arg1, arg2]

    with pytest.raises(exceptions.PathNotExistException):
        settings = parseArgument()

def test_parseArgumentThrowsWhenArg2DoesNotExist():
    arg1 = str( TESTDATA_DIR / 'userlists' / 'list1.txt' )
    arg2 = str( TESTDATA_DIR / 'NONEXISTANT' )
    sys.argv = [sys.argv[0], arg1, arg2]

    with pytest.raises(exceptions.PathNotExistException):
        settings = parseArgument()