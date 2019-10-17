from pathlib import Path
import shutil
import sys

import pytest
    
PROJECT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_DIR / 'src'
TEST_FILES_LOCATION = PROJECT_DIR / 'testdata' / 'userlists'

sys.path.append(str( SRC_DIR ))

import exceptions
from readUserList import getList, readUserList

def test_getList_ShouldReturnListOfSize3():
    filePath = TEST_FILES_LOCATION / 'list1.txt'

    filecontent = getList(filePath)
    assert len( filecontent ) == 3
    assert filecontent[0] == 'foo\n'
    assert filecontent[1] == 'bar\n'
    assert filecontent[2] == 'baz_'

def test_getList_ShouldIncludeEmptyLines():
    filePath = TEST_FILES_LOCATION / 'listwithemptylines.txt'

    filecontent = getList(filePath)
    assert len( filecontent ) == 5

def test_getList_ShouldThrowErrorWhenFIleNotExist():
    filePath = TEST_FILES_LOCATION / 'NON_EXISTANT_FILE.txt'

    with pytest.raises(exceptions.FileOpenErrorException):
        filecontent = getList(filePath)

def test_readUserList_ShouldTrimNewLine():
    filePath = TEST_FILES_LOCATION / 'manypatterns.txt'

    userList = readUserList(filePath)
    assert userList[0] == 'nonewline_'

def test_readUserList_ShouldTrimLeadingAndTrailingWhitespaces():
    filePath = TEST_FILES_LOCATION / 'manypatterns.txt'

    userList = readUserList(filePath)
    assert userList[1] == 'noleadingspaces'
    assert userList[2] == 'notrailingspaces'

def test_readUserList_ShouldTrimLeadingAtMark():
    filePath = TEST_FILES_LOCATION / 'manypatterns.txt'

    userList = readUserList(filePath)
    assert userList[3] == 'noleadingatmark'

def test_readUserList_ShouldIgnoreInvalidUsernames():
    filePath = TEST_FILES_LOCATION / 'manypatterns.txt'

    userList = readUserList(filePath)
    assert len(userList) == 4