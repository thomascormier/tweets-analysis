#from api import API
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='root',
    database='twitterdb')



class DataBase :
    def __init__(self):
        self.listFollowers = []
        self.listTweets = []
        #self.api = API("_agricool")
        self.mycursor = mydb.cursor()


    def buildDB(self,screen_name,name):
        self.createDB()
        self.fillFollowerInDB(screen_name,name)

    def createDB(self):
        """
        Delete the entire database and create a new empty one
        """
        self.mycursor.execute("DROP TABLE follower")
        createFollowerTable = "CREATE TABLE follower (" \
                                "screen_name VARCHAR(255)," \
                                "name varchar(255)," \
                                "PRIMARY KEY(screen_name)" \
                              ")"


        self.mycursor.execute(createFollowerTable)

        mydb.commit()

    #TODO : récupérer la ListFollowers
    def fillDB(self):
        """
        Parcours les followers récupérés un par un et les ajoute à la DB puis
        Parcous leurs tweets respectifs et les ajoute à la DB
        :return:
        """


    def fillFollowerInDB(self,screen_name,name):
        """
        Insert a Follower into the database
        """
        sqlInsertFollowers = "INSERT INTO follower (screen_name, name) VALUES (%s,%s)"
        args = (screen_name, name)
        self.mycursor.execute(sqlInsertFollowers,args)
        mydb.commit()

    def fillTweetInDB(self):
        """
        Insert a Tweet into the database
        """
        sqlInsertTweets = "INSERT INTO tweet content VALUES %s"
        self.mycursor.executemany(sqlInsertTweets,self.content)
        mydb.commit()

    def getFollowersdb(self):
        sqlInsertFollowers = "SELECT * from twitterdb.follower;"
        self.mycursor.execute(sqlInsertFollowers)
        records = self.mycursor.fetchall()
        print("Total number of rows in python_developers is - ", self.mycursor.rowcount)
        print("Printing each row's column values i.e.  developer record")
        for row in records:
            print("Id = ", row[0], )
            print("Name = ", row[1], "\n")

 # Constuit la DataBase