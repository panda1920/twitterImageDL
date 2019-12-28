from pathlib import Path
import shutil
import sys

import pytest
    
PROJECT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_DIR / 'src'

sys.path.append(str( SRC_DIR ))

from retrieve_twitterAPI import TweetsRetrieve_TwitterAPI
from retrieve_scraper import TweetsRetrieve_ScraperAPI

TEST_USERNAME = 'poopoopanda21'

@pytest.fixture(scope='function', params=[TweetsRetrieve_TwitterAPI, TweetsRetrieve_ScraperAPI])
def classToTest(request):
    yield request.param
    
def test_retrieveTweetsInfo(classToTest):
    tweets = classToTest().getTweetsInfo(TEST_USERNAME)

    assert len(tweets) == 3
    for tweet in tweets:
        images = tweet['images']
        assert len(images) > 0
        assert type(images[0]) is str