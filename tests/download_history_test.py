from pathlib import Path
import shutil
import sys
import json
import datetime
import re

import pytest

from twitter_image_dl.download_history import DownloadHistory
    
PROJECT_DIR = Path(__file__).resolve().parents[1]
HISTORY_DIR = PROJECT_DIR / 'testdata' / 'history'

HISTORYFILE_EXIST = HISTORY_DIR / 'history_exist.json'
HISTORYFILE_NOTYETEXIST = HISTORY_DIR / 'history_notyet.json'
TESTHISTORIES = {
    'user1': { 'tweetId': 'user1_1111', 'lastUpdate': '112233'},
    'user2': { 'tweetId': 'user2_2222', 'lastUpdate': '112233'},
    'user3': { 'tweetId': 'user3_3333', 'lastUpdate': '112233'},
    'user4': { 'tweetId': 'user4_4444', 'lastUpdate': '112233'},
}

@pytest.fixture(scope='function')
def clearTestDIr():
    yield
    if HISTORYFILE_EXIST.exists():
        HISTORYFILE_EXIST.unlink()
    if HISTORYFILE_NOTYETEXIST.exists():
        HISTORYFILE_NOTYETEXIST.unlink()

@pytest.fixture(scope='function')
def createTestFile():
    with Path(HISTORYFILE_EXIST).open('w') as f:
        json.dump(TESTHISTORIES, f)

class Test_DownloadHistory:
    def test_downloadHistoryConstruction(self, clearTestDIr, createTestFile):
        DownloadHistory(HISTORYFILE_EXIST)
        DownloadHistory(HISTORYFILE_NOTYETEXIST)

    def test_UpdateHistory(self, clearTestDIr):
        history = DownloadHistory(HISTORYFILE_NOTYETEXIST)
        history.updateHistory('user1', '112233')

    def test_updateHistoryShouldUpdateLastUpdate(self, clearTestDIr, createTestFile):
        history = DownloadHistory(HISTORYFILE_NOTYETEXIST)
        lastupdatePattern = re.compile(r'^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d$')
        
        history.updateHistory('user1', '112233')

        lastupdate = history._history['user1']['lastUpdate']
        assert lastupdate != TESTHISTORIES['user1']['lastUpdate']
        assert lastupdatePattern.match(lastupdate)

    def test_GetHistoryFromNonExistantHistory(self, clearTestDIr):
        history = DownloadHistory(HISTORYFILE_NOTYETEXIST)
        assert history.getHistory('user1') ==  None

        history.updateHistory('user1', '112233')
        assert history.getHistory('user1') == '112233'

        history.updateHistory('user1', '2')
        history.updateHistory('user1', '3')
        history.updateHistory('user1', '4')
        assert history.getHistory('user1') == '4'

    def test_getHistoryFromExistingHistory(self, clearTestDIr, createTestFile):
        history = DownloadHistory(HISTORYFILE_EXIST)
        for username in TESTHISTORIES.keys():
            assert history.getHistory(username) == TESTHISTORIES[username]['tweetId']

        history.updateHistory('user1', '2')
        history.updateHistory('user1', '3')
        history.updateHistory('user1', '4')
        assert history.getHistory('user1') == '4'

    def test_writeToFileForNonExistantHistory(self, clearTestDIr, createTestFile):
        history = DownloadHistory(HISTORYFILE_NOTYETEXIST)
        usernames = ['user1', 'user2', 'user3']
        tweetIds = ['1111', '2222', '3333']

        for username, tweetId in zip(usernames, tweetIds):
            history.updateHistory(username, tweetId)
        history.writeToFile()

        assert Path(HISTORYFILE_NOTYETEXIST).exists()
        with Path(HISTORYFILE_NOTYETEXIST).open('r', encoding='utf-8') as file:
            contentJson = json.load(file)
            
            for username, tweetId in zip(usernames, tweetIds):
                assert contentJson[username]['tweetId'] == tweetId

    def test_writeToFileForExistingHistory(self, clearTestDIr, createTestFile):
        history = DownloadHistory(HISTORYFILE_EXIST)
        usernames = ['user1', 'user2', 'user3']
        tweetIds = ['1--1--1', '2--2--2', '3--3--3']

        for username, tweetId in zip(usernames, tweetIds):
            history.updateHistory(username, tweetId)
        history.writeToFile()

        assert Path(HISTORYFILE_EXIST).exists()
        with Path(HISTORYFILE_EXIST).open('r', encoding='utf-8') as file:
            contentJson = json.load(file)
            
            for username, tweetId in zip(usernames, tweetIds):
                assert contentJson[username]['tweetId'] == tweetId
