from pathlib import Path
from unittest.mock import create_autospec
import shutil
import sys
import json
import datetime
import re

import pytest

from twitter_image_dl.download_history import DownloadHistory
from twitter_image_dl.runtime_bindings import RuntimeBindings
import twitter_image_dl.global_constants as constants
    
PROJECT_DIR = Path(__file__).resolve().parents[1]
HISTORY_DIR = PROJECT_DIR / 'testdata' / 'history'

TESTHISTORIES = {
    'user1': { 'tweetId': 'user1_1111', 'lastUpdate': '112233'},
    'user2': { 'tweetId': 'user2_2222', 'lastUpdate': '112233'},
    'user3': { 'tweetId': 'user3_3333', 'lastUpdate': '112233'},
    'user4': { 'tweetId': 'user4_4444', 'lastUpdate': '112233'},
}

@pytest.fixture(scope='function')
def setup_tmp_path(tmp_path):
    with Path(tmp_path / constants.FILENAME_HISTORY).open('w') as f:
        json.dump(TESTHISTORIES, f)

    return tmp_path

class Test_DownloadHistory:
    def test_downloadHistoryConstruction(self, setup_tmp_path):
        DownloadHistory()

    def test_downloadHistoryConstruction_whenNotExist(self, tmp_path):
        DownloadHistory()

    def test_UpdateHistory(self, tmp_path, ):
        history = DownloadHistory()
        history.updateHistory('user1', '112233')

        assert history.getHistory('user1') == '112233'

    def test_updateHistoryShouldUpdateLastUpdate(self, tmp_path):
        history = DownloadHistory()
        lastupdatePattern = re.compile(r'^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d$')
        
        history.updateHistory('user1', '112233')

        lastupdate = history._history['user1']['lastUpdate']
        assert lastupdate != TESTHISTORIES['user1']['lastUpdate']
        assert lastupdatePattern.match(lastupdate)

    def test_GetHistoryFromNonExistantHistory(self, tmp_path):
        history = DownloadHistory()
        assert history.getHistory('user1') ==  None

        history.updateHistory('user1', '112233')
        assert history.getHistory('user1') == '112233'

        history.updateHistory('user1', '2')
        history.updateHistory('user1', '3')
        history.updateHistory('user1', '4')
        assert history.getHistory('user1') == '4'

    def test_getHistoryFromExistingHistory(self, setup_tmp_path):
        history = DownloadHistory()
        history.loadFromFile(setup_tmp_path / constants.FILENAME_HISTORY)
        for username in TESTHISTORIES.keys():
            assert history.getHistory(username) == TESTHISTORIES[username]['tweetId']

        history.updateHistory('user1', '2')
        history.updateHistory('user1', '3')
        history.updateHistory('user1', '4')
        assert history.getHistory('user1') == '4'

    def test_writeToFileForNonExistantHistory(self, tmp_path):
        history = DownloadHistory()
        usernames = ['user1', 'user2', 'user3']
        tweetIds = ['1111', '2222', '3333']
        history_path = tmp_path / constants.FILENAME_HISTORY

        assert not history_path.exists()

        for username, tweetId in zip(usernames, tweetIds):
            history.updateHistory(username, tweetId)
        history.writeToFile(history_path)

        assert history_path.exists()
        with history_path.open('r', encoding='utf-8') as file:
            contentJson = json.load(file)
            
            for username, tweetId in zip(usernames, tweetIds):
                assert contentJson[username]['tweetId'] == tweetId

    def test_writeToFileForExistingHistory(self, setup_tmp_path):
        history = DownloadHistory()
        usernames = ['user1', 'user2', 'user3']
        tweetIds = ['1--1--1', '2--2--2', '3--3--3']
        history_path = setup_tmp_path / constants.FILENAME_HISTORY

        history.loadFromFile(history_path)
        for username, tweetId in zip(usernames, tweetIds):
            history.updateHistory(username, tweetId)
        history.writeToFile(history_path)

        assert history_path.exists()
        with history_path.open('r', encoding='utf-8') as file:
            contentJson = json.load(file)
            
            for username, tweetId in zip(usernames, tweetIds):
                assert contentJson[username]['tweetId'] == tweetId
