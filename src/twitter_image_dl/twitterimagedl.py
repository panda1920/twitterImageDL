from pathlib import Path
import os

from twitter_image_dl.parseArgument import parseArgument
from twitter_image_dl.readUserList import readUserList
from twitter_image_dl.retrieve_twitterAPI import TweetsRetrieve_TwitterAPI
from twitter_image_dl.download import downloadMedia
from twitter_image_dl.download_history import DownloadHistory
from twitter_image_dl.settings import Settings
import twitter_image_dl.setting_strings as strings
import twitter_image_dl.exceptions as exceptions

MEDIATYPES = ['images', 'gifs', 'videos']

def dlmedia():
    # settings = parseArgument()
    print(os.getcwd())
    settings = get_settings()
    paths = generate_paths(settings)
    users = readUserList(paths['userslist_filepath'])
    history = DownloadHistory(paths['history_filepath'])
    tweetsRetrieve = TweetsRetrieve_TwitterAPI(history, settings)

    for user in users:
        tweets = tweetsRetrieve.getTweetsInfo(user)
        downloadUserMedia(paths['save_location'], tweets, user)
    
    history.writeToFile()

def get_settings():
    settings = Settings( Path(os.getcwd()) / 'settings.conf' )
    validateSettings(settings)
    return settings

def generate_paths(settings):
    save_location = Path( settings.get()[strings.APP_SECTION][strings.SAVE_LOCATION] )
    return dict(
        save_location=save_location,
        userslist_filepath=(save_location / 'users.txt'),
        history_filepath=(save_location / 'history.json'),
    )

def validateSettings(settings):
    app_settings = settings.get()
    if (
        app_settings[strings.API_SECTION][strings.ACCESS_TOKEN] == '' or
        app_settings[strings.API_SECTION][strings.ACCESS_SECRET] == '' or
        app_settings[strings.API_SECTION][strings.CONSUMER_KEY] == '' or
        app_settings[strings.API_SECTION][strings.CONSUMER_SECRET] == ''
    ):
        raise exceptions.APINotFound('Please make sure to fill out twitter API related options in settings')
    if (
        not Path(app_settings[strings.APP_SECTION][strings.SAVE_LOCATION]).exists()
    ):
        raise exceptions.SaveLocationNotExist('Please make sure to specify a valid save location in settings')

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
