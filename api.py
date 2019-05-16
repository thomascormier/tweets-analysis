import follower
import tokenizer
import tweet

import tweepy
import logging

try:
    import json
except ImportError:
    import simplejson as json

logging.basicConfig()
from datetime import datetime, timedelta

######################################API SETTINGS########################################

ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

##########################################################################################

class API :
    def __init__(self,idAccount):
        self.idAccount = idAccount
        self.FollowersIDs = self.getFollowersIDs(idAccount)


    def getFollowersIDs(self, idAccount):
        """
        :param idAccount: La compte dont on souhaite récupérer les followers
        :return: Une liste des followers d'un compte
        """
        listIDs = []
        for ids in tweepy.Cursor(api.followers_ids, id=idAccount).items(2):
            listIDs.append(ids)
        return listIDs

    def setDateT(self,dateTweet):
        monthsDic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                     "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        dateToString = dateTweet[8:10] + "/" + monthsDic[dateTweet[4:7]] + "/" + dateTweet[-2:]
        d = datetime.strptime(dateToString, "%d/%m/%y")
        h = dateTweet[dateTweet.find(':') - 2:dateTweet.find(':')]
        m = dateTweet[dateTweet.find(':') + 1:dateTweet.find(':') + 3]
        d = d.replace(hour=int(h), minute=int(m))
        d = d + timedelta(hours=1)
        return d

    def indexFollower(self,listFollowers, id):
        res = {}
        for i in range(len(listFollowers)):
            if listFollowers[i].idF == id:  # check if the follower is already in the list
                res = {False: i}
                return res
        res = {True: len(listFollowers)}
        return res

    def getlistFollowers(self,ids):
        listFollowers = []
        for i in range(len(ids)):
            # Pour chaque follower sélectionné
            for status in tweepy.Cursor(api.user_timeline, screen_name=api.get_user(ids[i]).screen_name,tweet_mode='extended').items(2):
                # On parcoure ces 2 derniers tweets pour récupérer les infos suivantes :

                tweetFeed = status._json
                date = self.setDateT(tweetFeed['created_at'])  # when the tweet posted
                content = tweetFeed['full_text']  # content of the tweet
                screen_name = api.get_user(ids[i]).screen_name
                res = self.indexFollower(listFollowers, ids[i])

                if next(iter(res)):
                    listFollowers.append(follower.Follower(ids[i], screen_name))
                    listFollowers[res[True]].addTweet(tweet.Tweet(date, content, tokenizer.getWeight(content)))
                else:
                    listFollowers[res[False]].addTweet(tweet.Tweet(date, content, tokenizer.getWeight(content)))

        return listFollowers


twitterAPI = API("_agricool")
companyFollowerIDs = twitterAPI.FollowersIDs

print("============ID des followers récupérés============\n", companyFollowerIDs)

listFollowers = twitterAPI.getlistFollowers(companyFollowerIDs)