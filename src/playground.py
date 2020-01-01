from unittest.mock import create_autospec
from pathlib import Path
import json

from retrieve_twitterAPI import TweetsRetrieve_TwitterAPI
from download_history import DownloadHistory

historyMock = create_autospec(DownloadHistory)
historyMock.getHistory.return_value = None

retrieve = TweetsRetrieve_TwitterAPI(historyMock)
tweets = retrieve.getAllTweetsFromUser('poopoopanda21')

savePath = Path(__file__).absolute().parents[1] / 'testdata' / 'tweets.json'
with savePath.open('w') as f:
    json.dump(tweets, f)