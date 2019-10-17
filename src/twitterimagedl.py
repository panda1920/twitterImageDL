from parseArgument import parseArgument
from readUserList import readUserList
from retrieve_scraper import TweetsRetrieve_ScraperAPI
from download import downloadImages

def dlimage():
    settings = parseArgument()
    users = readUserList(settings['usersListPath'])
    
    for user in users:
        tweets = TweetsRetrieve_ScraperAPI().getTweetsInfo(user)
        images = getImagesList(tweets)

        downloadImages(
            images,
            user,
            settings['saveLocation']
        )

def getImagesList(tweets):
    images = []
    for tweet in tweets:
        images += tweet['images']

    return images

if __name__ == '__main__':
    dlimage()