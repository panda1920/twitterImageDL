import urllib.request
import json
import os
import os.path

from bs4 import BeautifulSoup

class TweetsRetrieve_ScraperAPI:
    SCRAPERAPI_KEY = os.environ['SCRAPERAPI_KEY']
    TEST_HTML = os.path.join( os.path.dirname(os.path.abspath(__file__)), '..\\testdata\\twitterpage2.html' )
    def __init__(self):
        pass

    def getTweetsInfo(self, username):        
        return list( map(self.getTweetInfo, self.getTweets(username)) )

    def getTweets(self, username):
        soup = BeautifulSoup( self.getTwitterPage(username), 'html.parser' )
        return soup.find_all(attrs={ 'class': 'js-stream-item' }, name='li')

    def getTweetInfo(self, tweet):
        tweetinfo = {
            'text': self.getText(tweet),
            'timestamp': self.getTimestamp(tweet),
            'images': self.getImages(tweet),
        }
        return tweetinfo

    def getTimestamp(self, tweet):
        timeSection = tweet.find(name='span', attrs={'class': '_timestamp'})
        return timeSection['data-time']

    def getText(self, tweet):
        textSection = tweet.find(name='p', attrs={ 'class': 'js-tweet-text'})
        text = ''
        for string in textSection.strings:
            text += string
        return text

    def getImages(self, tweet):
        images = tweet.find_all(attrs={'class': 'AdaptiveMedia-photoContainer'})
        geturl = lambda image: image['data-image-url']
        return list( map(geturl, images) )

    def getTwitterPage(self, username):
        with urllib.request.urlopen( self.getTwitterPageURL(username) ) as res:
            body = res.read().decode('utf-8')
            return body

    def getTwitterPageURL(self, username):
        return f'http://api.scraperapi.com?api_key={self.SCRAPERAPI_KEY}&url=https://twitter.com/{username}/media'