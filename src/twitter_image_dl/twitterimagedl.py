from pathlib import Path

from twitter_image_dl.parseArgument import parseArgument
from twitter_image_dl.runtime_bindings import RuntimeBindings

MEDIATYPES = ['images', 'gifs', 'videos']

def dlmedia(bindings):
    # settings = parseArgument()
    users = bindings.get_users()

    for user in users:
        tweets = bindings.get_tweet_retriever().getTweetsInfo(user)
        downloadUserMedia(bindings, tweets, user)
    
    bindings.get_history().writeToFile()

def downloadUserMedia(bindings, tweets, username):
    userSavePath = createAndReturnPath(bindings.get_save_location(), username)

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
