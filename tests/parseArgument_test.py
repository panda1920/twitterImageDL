from pathlib import Path
import shutil
import sys

import pytest

import twitter_image_dl.exceptions as exceptions
from twitter_image_dl.parseArgument import parseArgument
    
PROJECT_DIR = Path(__file__).resolve().parents[1]
TESTDATA_DIR = PROJECT_DIR / 'testdata'
sysArgs = []

@pytest.fixture(scope='function')
def restoreSysArgs():
    sysArgs = sys.argv
    yield
    sys.argv = sysArgs

def test_parseArgumentReturnsObjectWhenArgCountBT2(restoreSysArgs):
    arg1 = str( TESTDATA_DIR / 'userlists' / 'list1.txt' )
    arg2 = str( TESTDATA_DIR / 'download' )
    arg3 = str( TESTDATA_DIR / 'history' / 'history.txt' )
    sys.argv = [sys.argv[0], arg1, arg2, arg3]

    settings = parseArgument()
    assert 'usersListPath' in settings
    assert 'historyPath' in settings
    assert 'saveLocation' in settings
    assert settings['usersListPath'] == arg1
    assert settings['saveLocation'] == arg2
    assert settings['historyPath'] == arg3

def test_parseArgumentThrowsWhenArgCountIsOne(restoreSysArgs):
    arg1 = str( TESTDATA_DIR / 'userlists' / 'list1.txt' )
    sys.argv = [sys.argv[0], arg1]

    with pytest.raises(exceptions.InvalidArgumentCountException):
        settings = parseArgument()

def test_parseArgumentThrowsWhenArgCountIsTwo(restoreSysArgs):
    arg1 = str( TESTDATA_DIR / 'userlists' / 'list1.txt' )
    arg2 = str( TESTDATA_DIR / 'download' )

    with pytest.raises(exceptions.InvalidArgumentCountException):
        settings = parseArgument()

def test_parseArgumentThrowsWhenArg1DoesNotExist(restoreSysArgs):
    arg1 = str( TESTDATA_DIR / 'nonexistant' / 'file.txt' )
    arg2 = str( TESTDATA_DIR / 'download' )
    arg3 = str( TESTDATA_DIR / 'history' / 'history.txt' )
    sys.argv = [sys.argv[0], arg1, arg2, arg3]

    with pytest.raises(exceptions.PathNotExistException):
        settings = parseArgument()

def test_parseArgumentThrowsWhenArg2DoesNotExist(restoreSysArgs):
    arg1 = str( TESTDATA_DIR / 'userlists' / 'list1.txt' )
    arg2 = str( TESTDATA_DIR / 'NONEXISTANT' )
    arg3 = str( TESTDATA_DIR / 'history' / 'history.txt' )
    sys.argv = [sys.argv[0], arg1, arg2, arg3]

    with pytest.raises(exceptions.PathNotExistException):
        settings = parseArgument()

def test_parseArgumentDoesNotThrowWhenArg3DoesNotExist(restoreSysArgs):
    arg1 = str( TESTDATA_DIR / 'userlists' / 'list1.txt' )
    arg2 = str( TESTDATA_DIR / 'download' )
    arg3 = str( TESTDATA_DIR / 'history' / 'non_existant_file.txt' )
    sys.argv = [sys.argv[0], arg1, arg2, arg3]

    settings = parseArgument()
