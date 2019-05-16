from api import API

import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    database='twitterdb')

mycursor = mydb.cursor()



class DataBase :
    def __init__(self):
        self.listFollowers = []
        self.listTweets = []
        self.api = API("_agricool")

    def buildDB(self):
        self.createDB()
        self.fillDB()

    def createDB(self):
        """
        Delete the entire database and create a new empty one
        """
        mycursor.execute("DROP TABLE tweet")
        mycursor.execute("DROP TABLE follower")

        createFollowerTable = "CREATE TABLE follower (" \
                                "idF VARCHAR(255)," \
                                "screen_name varchar(255)," \
                                "weight int(10)," \
                                "PRIMARY KEY(idF)" \
                              ")"

        createTweetTable = "CREATE TABLE tweet (" \
                            "idT VARCHAR(255)," \
                            "idF VARCHAR(255)," \
                            "type VARCHAR(255)," \
                            "content VARCHAR(140)," \
                            "weight INTEGER(10)," \
                            "PRIMARY KEY(idT)," \
                            "FOREIGN KEY (idF) REFERENCES follower(idF)" \
                           ")"

        mycursor.execute(createFollowerTable)
        mycursor.execute(createTweetTable)

    #TODO : récupérer la ListFollowers
    def fillDB(self):
        """
        Parcours les followers récupérés un par un et les ajoute à la DB puis
        Parcous leurs tweets respectifs et les ajoute à la DB
        :return:
        """
        for follower in self.api.listFollowers:
            follower.fillFollowerInDB()
            self.listFollowers.append(follower)
            for tweet in follower.listTweets:
                tweet.fillTweetInDB()
                self.listFollowers.append(follower)

    def fillFollowerInDB(self):
        """
        Insert a Follower into the database
        """
        sqlInsertFollowers = "INSERT INTO follower screen_name VALUES %s"
        mycursor.execute(sqlInsertFollowers,self.screen_name)
        mydb.commit()

    def fillTweetInDB(self):
        """
        Insert a Tweet into the database
        """
        sqlInsertTweets = "INSERT INTO tweet content VALUES %s"
        mycursor.executemany(sqlInsertTweets,self.content)
        mydb.commit()


mydb = DataBase()
mydb.createDB() # Constuit la DataBase