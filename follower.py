class Follower :
    def __init__(self,idF,sceeen_name):
        self.idF = idF
        self.screen_name = sceeen_name
        self.listTweets = []
        self.weight = 0

    def addTweet(self,tweet):
        self.listTweets.append(tweet)

    def updateWeightFollower(self):
        for tweet in self.listTweets:
            self.weight+=tweet.weight