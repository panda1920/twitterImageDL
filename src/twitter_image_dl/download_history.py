import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class DownloadHistory:
    """
    A class that keeps track of the latest tweet that was downloaded in the past.
    Used to reduce unnecessary api calls to twitter.
    """

    def __init__(self):
        logger.info('Initializing history object')

        self._history = {}

        logger.info('Finished initializing history object')

    def loadFromFile(self, filepath):
        logger.info('Loading history from file %s', str(filepath))

        if not filepath.exists():
            self._history = {}
            logger.warning('Failed to load from file %s', str(filepath))
            return

        with filepath.open('r', encoding='utf-8') as f:
            self._history = json.load(f)

    def updateHistory(self, username, tweetId):
        logger.debug('Updating history of user %s', username)

        currentTimeString = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self._history[username] = {
            'tweetId': tweetId,
            'lastUpdate': currentTimeString,
        }

    def getHistory(self, username):
        logger.debug('Retrieving history of user %s', username)

        if username in self._history:
            return self._history[username]['tweetId']
        else:
            return None

    def writeToFile(self, filepath):
        logger.info('Updating history file %s', str(filepath))

        with filepath.open('w', encoding='utf-8') as f:
            json.dump(self._history, f)
