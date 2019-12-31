from pathlib import Path
import shutil
import sys
from unittest.mock import create_autospec

import pytest
    
PROJECT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_DIR / 'src'

sys.path.append(str( SRC_DIR ))

from retrieve_scraper import TweetsRetrieve_ScraperAPI
from retrieve_twitterAPI import TweetsRetrieve_TwitterAPI
from download_history import DownloadHistory

TEST_USERNAME = 'poopoopanda21'
MOST_RECENT_TWEET_ID = '1181518802422382593'

@pytest.fixture(scope='function')
def mockHistory():
    yield create_autospec(DownloadHistory)

def test_retrieveTweetsWithScraper():
    tweets = TweetsRetrieve_ScraperAPI().getTweetsInfo(TEST_USERNAME)

    assert len(tweets) == 3
    for tweet in tweets:
        images = tweet['images']
        assert len(images) > 0
        assert type(images[0]) is str
        
def test_retrieveTweetsWithAPI(mockHistory):
    mockHistory.getHistory.return_value = None
    tweets = TweetsRetrieve_TwitterAPI(mockHistory).getTweetsInfo(TEST_USERNAME)

    assert len(tweets) == 3
    for tweet in tweets:
        images = tweet['images']
        assert len(images) > 0
        assert type(images[0]) is str

    assert mockHistory.getHistory.call_count == 1
    arg1Passed = mockHistory.getHistory.call_args[0][0]
    assert arg1Passed == TEST_USERNAME

    assert mockHistory.updateHistory.call_count == 1
    arg1Passed = mockHistory.updateHistory.call_args[0][0]
    arg2Passed = mockHistory.updateHistory.call_args[0][1]
    assert arg1Passed == TEST_USERNAME
    assert arg2Passed == MOST_RECENT_TWEET_ID

def test_retrieveTweetsWithAPIWhereSince_idMoreRecentThatNewestTweet(mockHistory):
    mockHistory.getHistory.return_value = MOST_RECENT_TWEET_ID
    tweets = TweetsRetrieve_TwitterAPI(mockHistory).getTweetsInfo(TEST_USERNAME)

    assert len(tweets) == 0

    assert mockHistory.getHistory.call_count == 1
    arg1Passed = mockHistory.getHistory.call_args[0][0]
    assert arg1Passed == TEST_USERNAME

    assert mockHistory.updateHistory.call_count == 0