from pathlib import Path
import pdb
import logging

from twitter_image_dl.parseArgument import parseArgument
from twitter_image_dl.runtime_bindings import RuntimeBindings
import twitter_image_dl.global_constants as constants

MEDIATYPES = ['images', 'gifs', 'videos']
logger = logging.getLogger(__name__)

def dlmedia(bindings):
    logger.info('Starting download task')

    bindings.get_settings().validate_settings()
    history_path = bindings.get_save_location() / constants.FILENAME_HISTORY
    bindings.get_history().loadFromFile(history_path)

    downloadUserMedia(bindings)
    
    bindings.get_history().writeToFile(history_path)

    logger.info('Finished download task')

def downloadUserMedia(bindings):
    users = bindings.get_users()

    for username in users:
        logger.info('Downloading medis from user %s', username)
        if bindings.get_abort().is_set():
            break
        
        userSavePath = createAndReturnPath(bindings.get_save_location(), username)
        tweets = bindings.get_tweet_retriever().getTweetsInfo(username)

        for mediaType in MEDIATYPES:
            mediaSavePath = createAndReturnPath(userSavePath, mediaType)
            mediaURLs = getFileURLsFromTweets(tweets, mediaType)
            bindings.download_media(mediaURLs, mediaSavePath)

def getFileURLsFromTweets(tweets, mediaType):
    logger.info('Extracting media file urls from tweets')

    fileURLs = []
    for tweet in tweets:
        fileURLs += tweet[mediaType]

    return fileURLs

def createAndReturnPath(*pathComponents):
    path = Path(*pathComponents)
    path.mkdir(exist_ok=True)
    return path
    
if __name__ == '__main__':
    dlmedia()
