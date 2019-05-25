import api
import csv

class CSVFile:
    def createCSV(self):
        data = []
        with open('data.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            for follower in TwitterAPI.listFollowers:
                for tweet in follower.listTweets:
                    if tweet.content.startswith("RT"):
                        type = 'RT'
                    else:
                        type = 'T'
                    data.append([type, str(tweet.date)])
        a.writerows(data)
        print(data)