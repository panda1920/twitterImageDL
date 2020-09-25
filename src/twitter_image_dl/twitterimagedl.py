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
    print('Starting download task...')

    try:
        bindings.get_settings().validate_settings()
        history_path = bindings.get_save_location() / constants.FILENAME_HISTORY
        bindings.get_history().loadFromFile(history_path)

        downloadUserMedia(bindings)
        
        bindings.get_history().writeToFile(history_path)
    except:
        logger.exception('Terminated download task due to an error')
        print('Terminated download task due to an error')

    logger.info('Finished download task')
    print('Download task finished!')

def downloadUserMedia(bindings):
    users = bindings.get_users()

    for username in users:
        if bindings.get_abort().is_set():
            logger.info('Terminating download task due to abort flag')
            break

        logger.info('Downloading files from user %s', username)
        print(f'Downloading from user {username}')
        
        userSavePath = createAndReturnPath(bindings.get_save_location(), username)
        tweets = bindings.get_tweet_retriever().getTweetsInfo(username)

        for mediaType in MEDIATYPES:
            mediaSavePath = createAndReturnPath(userSavePath, mediaType)
            mediaURLs = getFileURLsFromTweets(tweets, mediaType)
            bindings.download_media(mediaURLs, mediaSavePath)

def getFileURLsFromTweets(tweets, mediaType):
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
