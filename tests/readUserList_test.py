from pathlib import Path
import shutil
import sys

import pytest
    
import twitter_image_dl.exceptions as exceptions
from twitter_image_dl.readUserList import getList, readUserList

PROJECT_DIR = Path(__file__).resolve().parents[1]
TEST_FILES_LOCATION = PROJECT_DIR / 'testdata' / 'userlists'

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

def test_readUserList_ShouldBeEmptyListWhenFileNotExist():
    filePath = TEST_FILES_LOCATION / 'NON_EXISTANT_FILE.txt'

    userList = readUserList(filePath)
    assert len(userList) == 0
    
    filePath.unlink()

def test_readUserList_ShouldCreateUserListFileWhenFileNotExist():
    filePath = TEST_FILES_LOCATION / 'NON_EXISTANT_FILE.txt'
    assert not filePath.exists()

    readUserList(filePath)
    
    assert filePath.exists()
    filePath.unlink()

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

def test_readerList_ShouldIgnoreDuplicateNames():
    filePath = TEST_FILES_LOCATION / 'duplicates.txt'

    userList = readUserList(filePath)
    assert len(userList) == 3
