import follower
import tokenizer
import tweet

import tweepy
import logging
import csv
import time

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
        self.listFollowers = self.getlistFollowers()

    def getFollowersIDs(self, idAccount):
        """
        :param idAccount: La compte dont on souhaite récupérer les followers
        :return: Une liste des followers d'un compte
        """
        listIDs = []
        for ids in tweepy.Cursor(api.followers_ids, id=idAccount).items(0):
            listIDs.append(ids)
        return listIDs

    def getlistFollowers(self):
        ids = self.FollowersIDs
        listFollowers = []
        for i in range(len(ids)):
            # Pour chaque follower sélectionné
            for status in tweepy.Cursor(api.user_timeline, screen_name=api.get_user(ids[i]).screen_name,tweet_mode='extended').items(0):
                # On parcoure ces 2 derniers tweets pour récupérer les infos suivantes :
                soloTweet = status._json
                date = self.setDateT(soloTweet['created_at'])  # On calcule et on stocke la date du tweet
                content = soloTweet['full_text']  # On stocke le contenu du tweet
                screen_name = api.get_user(ids[i]).screen_name # On stocke le screen_name de propriétaire du tweet
                res = self.indexFollower(listFollowers, ids[i])

                if next(iter(res)):
                    # Si on ne connait pas le follower :
                    listFollowers.append(follower.Follower(ids[i], screen_name))
                    # On crée et on ajoute le follower
                    listFollowers[res[True]].addTweet(tweet.Tweet(date, content, tokenizer.getWeight(content)))
                    # On crée et on ajoute le tweet
                else:
                    # Si on connait pas follower :
                    listFollowers[res[False]].addTweet(tweet.Tweet(date, content, tokenizer.getWeight(content)))
                    # On crée et on ajoute le tweet

        return listFollowers

    def indexFollower(self,listFollowers, id):
        #res = {}
        for i in range(len(listFollowers)):
            if listFollowers[i].idF == id:  # check if the follower is already in the list
                res = {False: i}
                return res
        res = {True: len(listFollowers)}
        return res

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

#TwitterAPI = API("_agricool")

##########################################################################################

class CSVFile:
    def writeBasicCSV(self):
        data = []
        with open('BasicData.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            for follower in TwitterAPI.listFollowers:
                for tweet in follower.listTweets:
                    if tweet.content.startswith("RT"):
                        type = 'RT'
                    else:
                        type = 'T'
                    data.append([type, str(tweet.date)])
                    time.sleep(10)
            a.writerows(data)
            print(data)
            fp.close

    def writeFollowerCSV(self):
        data = []
        with open('ListFollowers.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            for follower in TwitterAPI.listFollowers:
                data.append([follower.screen_name])
                time.sleep(120)
            a.writerows(data)
            print(data)
            fp.close

    def writeTweetCSV(self):
        data = []
        with open('ListTweets.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            for follower in TwitterAPI.listFollowers:
                for tweet in follower.listTweets:
                    if tweet.content.startswith("RT"):
                        type = 'RT'
                    else:
                        type = 'T'
                    data.append([follower.screen_name,type, str(tweet.date)])
                    time.sleep(10)
            a.writerows(data)
            print(data)
            fp.close

#BasicCSV = CSVFile()
#BasicCSV.writeBasicCSV()

#FollowerdataCSV = CSVFile()
#FollowerdataCSV.writeFollowerCSV()

#TweetdataCSV = CSVFile()
#TweetdataCSV.writeTweetCSV()

##########################################################################################


