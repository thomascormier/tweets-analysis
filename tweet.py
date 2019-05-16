class Tweet:
    def __init__(self, date, content, weight):
        self.date = date
        self.content = content
        self.weight = weight
        self.type = self.tweetType()

    def tweetType(self):
        if self.content.startswith("RT"):
            return "RT"
        else:
            return "T"