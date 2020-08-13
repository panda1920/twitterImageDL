from pathlib import Path

from twitter_image_dl.parseArgument import parseArgument
from twitter_image_dl.readUserList import readUserList
from twitter_image_dl.retrieve_twitterAPI import TweetsRetrieve_TwitterAPI
from twitter_image_dl.download import downloadMedia
from twitter_image_dl.download_history import DownloadHistory

MEDIATYPES = ['images', 'gifs', 'videos']

def dlmedia():
    settings = parseArgument()
    users = readUserList(settings['usersListPath'])
    history = DownloadHistory(settings['historyPath'])
    tweetsRetrieve = TweetsRetrieve_TwitterAPI(history)

    for user in users:
        tweets = tweetsRetrieve.getTweetsInfo(user)
        downloadUserMedia(settings['saveLocation'], tweets, user)
    
    history.writeToFile()

def downloadUserMedia(saveLocation, tweets, username):
    userSavePath = createAndReturnPath(saveLocation, username)

    for mediaType in MEDIATYPES:
        mediaSavePath = createAndReturnPath(userSavePath, mediaType)
        mediaURLs = getFileURLsFromTweets(tweets, mediaType)
        downloadMedia(mediaURLs, mediaSavePath)

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
