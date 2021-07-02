import pymysql
#database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="youtube")
cursor = connection.cursor()
# Query for creating table
user = """CREATE TABLE user (
                            username varchar(30)  NOT NULL,
                            userId int(15) NOT NULL AUTO_INCREMENT,
                            pass varchar(15)  NOT NULL,
                            email varchar(30)  NOT NULL,
                            date varchar(30) ,
                            profileImage varchar(30),
                            PRIMARY KEY (userId)
)"""

video = """CREATE TABLE video (
                            videoId int(15) NOT NULL AUTO_INCREMENT,
                            videoName varchar(30)  NOT NULL,
                            vCaption text(50) NOT NULL,
                            time varchar(30)  NOT NULL,
                            data varchar(30)  NOT NULL,
                            thumbnail varchar(30),
                            views int(15) NOT NULL,
                            likes int(15) NOT NULL,
                            PRIMARY KEY (videoId),
                            FOREIGN KEY (videoId )
                                REFERENCES comment(videoId)
                                ON DELETE CASCADE
)"""

channel = """CREATE TABLE channel (
    channelId   int(15) NOT NULL AUTO_INCREMENT,
    userId      int(15) NOT NULL,
    channelName varchar(30) NOT NULL,
    date        varchar(30) NOT NULL,
    chCaption   text(50) NOT NULL,
    PRIMARY KEY (channelId),
    FOREIGN KEY (channelId )
        REFERENCES video(commentId)
        ON DELETE CASCADE
)"""

shareChannel = """CREATE TABLE shareChannel(
     userId  int(15) NOT NULL,
     videoId int(15) NOT NULL,
     channelId int(15) NOT NULL
)"""

view = """CREATE TABLE view(
     userId  int(15) NOT NULL,
     videoId int(15) NOT NULL
)"""

comment = """CREATE TABLE comment (
       userId int(15) NOT NULL,
       videoId int(30) NOT NULL,
       comment text(50) NOT NULL,
       commentId int(15) NOT NULL

)"""

likes = """CREATE TABLE likes (
     userId int(15) NOT NULL,
     videoId int(30) NOT NULL
)"""

joinChannel = """CREATE TABLE joinChannel(
        userId int(15) NOT NULL,
        channelId int(15) NOT NULL
)"""

playlist = """CREATE TABLE playlist(
         userId int(15) NOT NULL,
         videoId int(30) NOT NULL,
         playlistId int(15) NOT NULL,
         playlistName varchar(30) NOT NULL
)"""

cursor.execute(user)
cursor.execute(video)
cursor.execute(channel)
cursor.execute(shareChannel)
cursor.execute(view)
cursor.execute(likes)
cursor.execute(joinChannel)
cursor.execute(playlist)
connection.close()
