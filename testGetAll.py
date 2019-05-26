import time
import tweepy
import csv
from database2 import *
from pprint import pprint
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
    #for page in tweepy.Cursor(api.followers, screen_name=user_name).pages(1):
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
    #HEADERS = ["name", "screen_name"]
    db.createDB()
    with open(user_name + "_followers.csv", 'w',encoding="utf-8") as csvfile:
        for profile_data in data:
            screen_name = profile_data._json["screen_name"]
            name = profile_data._json["name"]
            db.fillFollowerInDB(screen_name,name)

def insertTweet(db):
    db.getFollowersdb()

if __name__ == '__main__':

    db= DataBase()
    #followers = get_followers("_agricool")
    #save_followers_to_db("_agricool", followers,db)
    insertTweet(db)