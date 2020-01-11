import urllib.request
import urllib.parse
from urllib.error import HTTPError
import json
import time

from twitterAPIAuthentication import createOAuth1HeaderString, createAuthInfo

class TweetsRetrieve_TwitterAPI:
    METHOD = 'GET'
    ENDPOINT_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    DEFAULT_QUERY_STRING = {
        'screen_name': None,
        'count': '200',
        'trim_user': 'true',
        'exclude_replies': 'true',
        'include_rts': 'false'
    }

    def __init__(self, history):
        self._history = history

    def getTweetsInfo(self, username):
        print(f'getting Tweets from {username}...')

        allTweets = self.getAllTweetsFromUser(username)

        return [
            self.makeTweetInfo(tweet) for tweet in allTweets
            if self.tweetHaveMedia(tweet)
        ]

    def makeTweetInfo(self, tweet):
        return {
            'text': tweet['text'],
            'timestamp': self.convertCreatedAtToEpochTime(tweet['created_at']),
            'images': self.extractImageURLsFromTweet(tweet),
            'videos': self.extractVideoURLsFromTweet(tweet),
            'gifs': self.extractGifURLsFromTweet(tweet),
        }

    def convertCreatedAtToEpochTime(self, createdAt):
        return time.mktime(time.strptime(createdAt,"%a %b %d %H:%M:%S +0000 %Y"))

    def extractImageURLsFromTweet(self, tweet):
        return [
            image['media_url'] for image in tweet['extended_entities']['media']
            if image['type'] == 'photo'
        ]
        
    def extractGifURLsFromTweet(self, tweet):
        return [
            gif['video_info']['variants'][0]['url'] for gif in tweet['extended_entities']['media']
            if gif['type'] == 'animated_gif'
        ]
        # url in tweet is in mp4 format for some reason...
        # might have to make some conversion function or calls to other micro service

    def extractVideoURLsFromTweet(self, tweet):
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

    def tweetHaveMedia(self, tweet):
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
        queryString = self.createQueryString(username, maxId, mostRecentTweetId)
        headers = self.createHeader(queryString)
        url = f'{self.ENDPOINT_URL}?{urllib.parse.urlencode(queryString)}'
        request = urllib.request.Request(url, headers=headers, method=self.METHOD)

        try:
            with urllib.request.urlopen(request) as response:
                tweets = json.loads( response.read() )
                return tweets
        except HTTPError:
            print(f'failed to retrieve tweet from user {username}')
            return []

    def createQueryString(self, username, maxId, mostRecentTweetId):
        queryString = self.DEFAULT_QUERY_STRING.copy()
        queryString['screen_name'] = username
        if maxId != None:
            queryString['max_id'] = str(maxId)
        if mostRecentTweetId != None:
            queryString['since_id'] = mostRecentTweetId

        return queryString

    def createHeader(self, queryString):
        return {
            'Authorization': createOAuth1HeaderString(
                self.ENDPOINT_URL,
                self.METHOD,
                queryString,
                {},
                createAuthInfo()
            ),
        }