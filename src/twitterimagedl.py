from parseArgument import parseArgument
from readUserList import readUserList
from retrieve_twitterAPI import TweetsRetrieve_TwitterAPI
from download import downloadImages
from download_history import DownloadHistory

def dlimage():
    settings = parseArgument()
    history = DownloadHistory(settings['historyPath'])
    tweetsRetrieve = TweetsRetrieve_TwitterAPI(history)
    users = readUserList(settings['usersListPath'])
    
    for user in users:
        tweets = tweetsRetrieve.getTweetsInfo(user)
        images = getImagesList(tweets)

        downloadImages(
            images,
            user,
            settings['saveLocation']
        )
    
    history.writeToFile()

def getImagesList(tweets):
    images = []
    for tweet in tweets:
        images += tweet['images']

    return images

if __name__ == '__main__':
    dlimage()