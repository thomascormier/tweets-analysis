import time
from datetime import datetime, timedelta

import tweepy
import csv
from database2 import *
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='root',
    database='twitterdb')
mycursor = mydb.cursor()

ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


def get_followers(user_name):
    """
    get a list of all followers of a twitter account
    :param user_name: twitter username without '@' symbol
    :return: list of usernames without '@' symbol
    """
    api = tweepy.API(auth)
    followers = []
    for page in tweepy.Cursor(api.followers, screen_name=user_name, wait_on_rate_limit=True,count=200).pages():
    #for page in tweepy.Cursor(api.followers, screen_name=user_name).pages(2):
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return followers


def save_followers_to_csv(user_name, data):
    """
    saves json data to csv
    :param data: data recieved from twitter
    :return: None
    """
    HEADERS = ["name", "screen_name"]
    with open(user_name + "_followers.csv", 'w',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(HEADERS)
        for profile_data in data:
            profile = []
            for header in HEADERS:
                profile.append(profile_data._json[header])
                print(profile_data._json[header])
            csv_writer.writerow(profile)



def save_followers_to_db(user_name, data,db):
    """
    saves json data in the database by creating followers identified by their screen_name
    :param data: data recieved from twitter
    :return: None
    """
    db.createDB() #!!!!ATTENTION !!!! CA DROP LES TABLES ATTENTION
    for profile_data in data:
        id = profile_data._json["id"]
        screen_name = profile_data._json["screen_name"]
        name = profile_data._json["name"]
        db.fillFollowerInDB(id,screen_name,name)


def insertTweet(db):
    records = db.getFollowersdb()
    api = tweepy.API(auth)
    followers = []
    i =0
    for row in records:
        if (i>100):
            break
        tweets = getTweetsFollower(row[0])
        for tweet in tweets:
            soloTweet = tweet._json
            date = setDateT(soloTweet['created_at'])  # On calcule et on stocke la date du tweet
            content = soloTweet['full_text']
            db.insertTweetdb(row[0],date,content)
        i+=1




def getTweetsFollower(followerId):
    tweets = []
    api = tweepy.API(auth)
    for status in tweepy.Cursor(api.user_timeline, screen_name=api.get_user(followerId).screen_name,tweet_mode="extended").items(3):
        try:
            tweets.append(status)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return tweets
#!!!!!!!!!!!!!!!!!!!!!!!!!!! TO DELETE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!





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



#!!!!!!!!!!!!!!!!!!!!!!!!!!! TO DELETE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if __name__ == '__main__':

    db= DataBase()

    followers = get_followers("_agricool")
    save_followers_to_db("_agricool", followers,db)
    insertTweet(db)
