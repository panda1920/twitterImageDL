import json
from datetime import datetime
from pathlib import Path

class DownloadHistory:
    """
    A class that keeps track of the latest tweet that was downloaded in the past.
    Used to reduce unnecessary api calls to twitter.
    """

    def __init__(self, historyPath):
        self._historyPath = Path(historyPath)
        self._history = self._loadHistory()

    def _loadHistory(self):
        if not self._historyPath.exists():
            return {}

        with self._historyPath.open('r', encoding='utf-8') as f:
            return json.load(f)

    def updateHistory(self, username, tweetId):
        currentTimeString = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self._history[username] = {
            'tweetId': tweetId,
            'lastUpdate': currentTimeString,
        }

    def getHistory(self, username):
        if username in self._history:
            return self._history[username]['tweetId']
        else:
            return None

    def writeToFile(self):
        with self._historyPath.open('w', encoding='utf-8') as f:
            json.dump(self._history, f)