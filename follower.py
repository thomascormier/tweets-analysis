class Follower :
    def __init__(self,idF,sceeen_name):
        self.idF = idF
        self.screen_name = sceeen_name
        self.listTweets = []

    def addTweet(self,tweet):
        self.listTweets.append(tweet)