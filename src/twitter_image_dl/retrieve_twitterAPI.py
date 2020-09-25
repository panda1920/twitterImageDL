import urllib.request
import urllib.parse
from urllib.error import HTTPError
import json
import time
import logging

from twitter_image_dl.twitterAPIAuthentication import createOAuth1HeaderString, createAuthInfo

logger = logging.getLogger(__name__)

class TweetsRetriever_TwitterAPI:
    METHOD = 'GET'
    ENDPOINT_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    DEFAULT_QUERY_STRING = {
        'screen_name': None,
        'count': '200',
        'trim_user': 'true',
        'exclude_replies': 'true',
        'include_rts': 'false'
    }

    def __init__(self, history, settings):
        logger.info('Initializting tweet retriever object')

        self._history = history
        self._settings = settings

        logger.info('Finished initializting tweet retriever object')

    def getTweetsInfo(self, username):
        logger.info('Retrieving tweets from user %s', username)

        allTweets = self.getAllTweetsFromUser(username)

        return [
            self._create_tweet_info(tweet) for tweet in allTweets
            if self._has_media(tweet)
        ]

    def _create_tweet_info(self, tweet):
        return {
            'text': tweet['text'],
            'timestamp': self._convertCreatedAtToEpochTime(tweet['created_at']),
            'images': self._extractImageURLs(tweet),
            'videos': self._extractVideoURLs(tweet),
            'gifs': self._extractGifURLs(tweet),
        }

    def _convertCreatedAtToEpochTime(self, createdAt):
        return time.mktime(time.strptime(createdAt,"%a %b %d %H:%M:%S +0000 %Y"))

    def _extractImageURLs(self, tweet):
        return [
            image['media_url'] for image in tweet['extended_entities']['media']
            if image['type'] == 'photo'
        ]
        
    def _extractGifURLs(self, tweet):
        return [
            gif['video_info']['variants'][0]['url'] for gif in tweet['extended_entities']['media']
            if gif['type'] == 'animated_gif'
        ]
        # url in tweet is in mp4 format for some reason...
        # might have to make some conversion function or calls to other micro service

    def _extractVideoURLs(self, tweet):
        # extracts the highest quality video from tweet
        videoVariants = [
            video['video_info']['variants'] for video in tweet['extended_entities']['media']
            if video['type'] == 'video'
        ]

        videos = []
        for variant in videoVariants:
            # there are several version of videos in the tweet;
            # I must find the one with the best quality
            bestQualityVideoSofar = { 'bitrate': 0 }
            for video in variant:
                if 'bitrate' in video and video['bitrate'] > bestQualityVideoSofar['bitrate']:
                    bestQualityVideoSofar = video
            
            url = bestQualityVideoSofar['url']
            # sometimes there is a weird ?tag=10 at the end so we remove it
            indexOfExtension = url.rfind('.mp4') + 4
            videos.append( url[:indexOfExtension] )

        return videos

    def _has_media(self, tweet):
        return 'extended_entities' in tweet

    def getAllTweetsFromUser(self, username):
        maxId = None # parameter used for pagination in twitter api
        mostRecentTweetId = self._history.getHistory(username)
        allTweets = []
        
        while True:
            tweets = self.getTweets(username, maxId, mostRecentTweetId)
            if len(tweets) == 0:
                break

            maxId = tweets[-1]['id'] - 1
            allTweets += tweets

        self.updateHistory(username, allTweets)
        return allTweets

    def updateHistory(self, username, allTweets):
        if len(allTweets) > 0:
            mostRecentTweetId = allTweets[0]['id_str']
            self._history.updateHistory(username, mostRecentTweetId)

    def getTweets(self, username, maxId, mostRecentTweetId):
        request = self._create_request_object(username, maxId, mostRecentTweetId)

        try:
            with urllib.request.urlopen(request) as response:
                return json.loads( response.read() )
        except HTTPError:
            logger.warning('Failed to retrieve tweet from user %s', username)
            print(f'Failed to retrieve tweets from user {username}: the user may not exist anymore')
            return []

    def _create_request_object(self, username, maxId, mostRecentTweetId):
        queryString = self.createQueryString(username, maxId, mostRecentTweetId)
        headers = self.createHeader(queryString)
        url = f'{self.ENDPOINT_URL}?{urllib.parse.urlencode(queryString)}'
        return urllib.request.Request(url, headers=headers, method=self.METHOD)

    def createQueryString(self, username, maxId, mostRecentTweetId):
        queryString = self.DEFAULT_QUERY_STRING.copy()
        queryString['screen_name'] = username
        if maxId != None:
            queryString['max_id'] = str(maxId)
        if mostRecentTweetId != None:
            queryString['since_id'] = mostRecentTweetId

        return queryString

    def createHeader(self, queryString):
        current_settings = self._settings.get()

        return {
            'Authorization': createOAuth1HeaderString(
                self.ENDPOINT_URL,
                self.METHOD,
                queryString,
                {},
                createAuthInfo(current_settings),
                current_settings
            ),
        }
