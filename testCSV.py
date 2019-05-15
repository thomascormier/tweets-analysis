import csv

with open('tweetdata.csv','w',newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    data = [['Date', 'Type'],
            ['date1', 'T'],
            ['date2', 'RT'],
            ['date3', 'RT'],
            ['date4', 'T']]
    a.writerows(data)