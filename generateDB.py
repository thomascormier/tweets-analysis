import mysql.connector

import follower
import tokenizer
import tweet

import csv
try:
    import json
except ImportError:
    import simplejson as json
import tweepy
import logging

logging.basicConfig()
from datetime import datetime, timedelta

###########################################API############################################

ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

#########################################DATABASE#########################################

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    database='twitterdb')

mycursor = mydb.cursor()

##########################################################################################


def getNFollowers(idAccount, nbFollowersToGet):
    """
    :param idAccount: La compte dont on souhaite récupérer les followers
    :return: Une liste des followers d'un compte
    """
    list = []
    for status in tweepy.Cursor(api.followers_ids, id=idAccount).items(nbFollowersToGet):
        list.append(status)
    return list


ids = getNFollowers("_agricool", 2)

print("============ID des followers récupérés============\n", ids)



def setDateT(dateTweet):
    monthsDic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                 "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    dateToString = dateTweet[8:10] + "/" + monthsDic[dateTweet[4:7]] + "/" + dateTweet[-2:]
    d = datetime.strptime(dateToString, "%d/%m/%y")
    h = dateTweet[dateTweet.find(':') - 2:dateTweet.find(':')]
    m = dateTweet[dateTweet.find(':') + 1:dateTweet.find(':') + 3]
    d = d.replace(hour=int(h), minute=int(m))
    d = d + timedelta(hours=1)
    return d


def indexFollower(listFollowers, id):
    res = {}
    for i in range(len(listFollowers)):
        if listFollowers[i].idF == id:  # check if the follower is already in the list
            res = {False: i}
            return res
    res = {True: len(listFollowers)}
    return res


def getlistFollowers(ids):
    listFollowers = []
    for i in range(len(ids)):
        # Pour chaque follower sélectionné
        for status in tweepy.Cursor(api.user_timeline, screen_name=api.get_user(ids[i]).screen_name,
                                    tweet_mode='extended').items(2):
            # On parcoure ces 2 derniers tweets pour récupérer les infos suivantes :
            tweetFeed = status._json
            date = setDateT(tweetFeed['created_at'])  # when the tweet posted
            content = tweetFeed['full_text']  # content of the tweet
            screen_name = api.get_user(ids[i]).screen_name
            res = indexFollower(listFollowers, ids[i])
            if next(iter(res)):
                listFollowers.append(follower.Follower(ids[i], screen_name))
                listFollowers[res[True]].addTweet(tweet.Tweet(date, content, tokenizer.getWeight(content)))
            else:
                listFollowers[res[False]].addTweet(tweet.Tweet(date, content, tokenizer.getWeight(content)))

    return listFollowers


listFollowers = getlistFollowers(ids)


data = []
with open('data.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')

    for follower in listFollowers:
        fillFollowerInDB()

        for tweet in follower.listTweets:
            tweet.getTweetType()




a.writerows(data)

print(data)







def getTweetType(self):
    if self.content.startswith("RT"):
        return 'RT'
    else:
        return 'T'


def createDB():
    """
    Delete the entire database and create a new empty one
    """
    mycursor.execute("DROP TABLE tweet")
    mycursor.execute("DROP TABLE follower")
    mycursor.execute("CREATE TABLE follower (idF VARCHAR(255), screen_name varchar(255), weight int(10),PRIMARY KEY(idF))")
    mycursor.execute("CREATE TABLE tweet (idT VARCHAR(255),idF VARCHAR(255), type VARCHAR(255), content VARCHAR(140),weight INTEGER(10),PRIMARY KEY(idT), FOREIGN KEY (idF) REFERENCES follower(idF))")


def fillFollowerInDB(self):
    sqlInsertFollowers = "INSERT INTO follower screen_name VALUES %s"
    mycursor.execute(sqlInsertFollowers,self.screen_name)
    mydb.commit()


def fillTweetInDB(self):
    sqlInsertTweets = "INSERT INTO tweet content VALUES %s"
    mycursor.executemany(sqlInsertTweets,self.content)
    mydb.commit()