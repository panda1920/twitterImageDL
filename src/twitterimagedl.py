from pathlib import Path
from parseArgument import parseArgument
from readUserList import readUserList
from retrieve_twitterAPI import TweetsRetrieve_TwitterAPI
from download import downloadMedia
from download_history import DownloadHistory

MEDIATYPES = ['images', 'gifs', 'videos']

def dlmedia():
    settings = parseArgument()
    history = DownloadHistory(settings['historyPath'])
    tweetsRetrieve = TweetsRetrieve_TwitterAPI(history)
    users = readUserList(settings['usersListPath'])
    for user in users:
        tweets = tweetsRetrieve.getTweetsInfo(user)
        downloadUserMedia(settings, tweets, user)
    
    history.writeToFile()

def downloadUserMedia(settings, tweets, username):
    userSavePath = createAndReturnPath(settings['saveLocation'], username)

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