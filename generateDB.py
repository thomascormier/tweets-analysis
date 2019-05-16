import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    database='twitterdb'
)

mycursor = mydb.cursor()

#mycursor.execute("DROP TABLE follower")
#mycursor.execute("DROP TABLE tweet")
#mycursor.execute("CREATE TABLE follower (idF VARCHAR(255), screen_name varchar(255), weight int(10),PRIMARY KEY(idF))")
#mycursor.execute("CREATE TABLE tweet (idT VARCHAR(255),idF VARCHAR(255), content VARCHAR(140),weight INTEGER(10),PRIMARY KEY(idT), FOREIGN KEY (idF) REFERENCES follower(idF))")

sqlFormula = "INSERT INTO follower (screen_name, weight) VALUES (%s,%s)"

for follower in listFollowers :
    followers = [(follower.screen_name,follower.weight)]

mycursor.executemany(sqlFormula, followers)

mydb.commit()