# Import the necessary package to process
#
# data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
#---------------------------------------------------------------------------------------------------------------------
# wait_on_rate_limit= True;  will make the api to automatically wait for rate limits to replenish
# wait_on_rate_limit_notify= Ture;  will make the api  to print a notification when Tweepyis waiting for rate limits to replenish
#---------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------
# The following loop will print most recent statuses, including retweets, posted by the authenticating user and that user’s friends.
# This is the equivalent of /timeline/home on the Web.
#---------------------------------------------------------------------------------------------------------------------


for status in tweepy.Cursor(api.home_timeline).items(50):
    tweet = status._json
    print(tweet)

    print("id : ", tweet['id']) # This is the tweet's id
    print("créer le : ", tweet['created_at']) # when the tweet posted
    print("contenu : ", tweet['text']) # content of the tweet
    print("id du compte : ", tweet['user']['id']) # id of the user who posted the tweet
    print("nom du user : ", tweet['user']['name']) # name of the user, e.g. "Wei Xu"
    print("nom du compte ", tweet['user']['screen_name'], "\n") # name of the user account, e.g. "cocoweixu"-----------------------------------------------------------------

#followers = tweepy.API.followers("ThomasB72832506")


def getFollowers(idAccount):
    c = tweepy.Cursor(api.followers_ids, id=idAccount)
    ids = []
    for page in c.pages():
        for p in page:
             ids.append(p)
    return ids


ids=getFollowers("_agricool")

listTest=[]
for i in range (10):
    listTest.append(ids[i])

print(listTest)
