import urllib.request
import urllib.parse
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

    def getTweetsInfo(self, username):
        allTweets = self.getAllTweetsFromUser(username)

        return [
            self.makeTweetInfo(tweet) for tweet in allTweets
            if self.tweetHaveMedia(tweet)
        ]

    def makeTweetInfo(self, tweet):
        return {
            'text': tweet['text'],
            'timestamp': self.convertCreatedAtToEpochTime(tweet['created_at']),
            'images': [
                image['media_url'] for image in tweet['extended_entities']['media']
                if image['type'] == 'photo'
            ],
            # 'videos': [
            #     video['media_url'] for video in tweet['extended_entities']['media']
            #     if video['type'] == 'video'
            # ],
            'gifs': [
                gifs['video_info']['variants']['url'] for gifs in tweet['extended_entities']['media']
                if gifs['type'] == 'animated_gif'
            ]
        }

    def convertCreatedAtToEpochTime(self, createdAt):
        return time.mktime(time.strptime(createdAt,"%a %b %d %H:%M:%S +0000 %Y"))

    def tweetHaveMedia(self, tweet):
        return 'extended_entities' in tweet

    def getAllTweetsFromUser(self, username):
        maxId = None # parameter used for pagination in twitter api
        allTweets = []
        
        while True:
            tweets = self.getTweets(username, maxId)
            numTweets = len(tweets)
            if numTweets == 0:
                return allTweets

            maxId = tweets[-1]['id'] - 1
            allTweets += tweets

    def getTweets(self, username, maxId):
        queryString = self.createQueryString(username, maxId)
        headers = self.createHeader(queryString)
        url = f'{self.ENDPOINT_URL}?{urllib.parse.urlencode(queryString)}'
        request = urllib.request.Request(url, headers=headers, method=self.METHOD)

        with urllib.request.urlopen(request) as response:
            tweets = json.loads( response.read() )
            return tweets

    def createQueryString(self, username, maxId):
        queryString = self.DEFAULT_QUERY_STRING.copy()
        queryString['screen_name'] = username
        if maxId != None:
            queryString['max_id'] = str(maxId)

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