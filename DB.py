import pymysql

# database connection
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
                            StorageId varchar (20) UNIQUE,
                            vCaption text(50) NOT NULL,
                            time varchar(30)  NOT NULL,
                            date varchar(30)  NOT NULL,
                            thumbnail varchar(30),
                            views int(15) NOT NULL,
                            likes int(15) NOT NULL,
                            dislikes int(15) NOT NULL,
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
    PRIMARY KEY (channelId)
)"""

shareChannel = """CREATE TABLE shareChannel(
     userId  int(15) NOT NULL,
     videoId int(15) NOT NULL,
     channelId int(15) NOT NULL,
     FOREIGN KEY (channelId) REFERENCES channel(channelId)
    ON DELETE CASCADE
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

commentOnComment = """CREATE TABLE commentOnComment  (
       parentCom int(15) NOT NULL,
       childCom int(15) NOT NULL,
       videoId int(30) NOT NULL

)"""

likes = """CREATE TABLE likes (
     userId int(15) NOT NULL,
     videoId int(30) NOT NULL
)"""

dislikes = """CREATE TABLE dislikes (
     userId int(15) NOT NULL,
     videoId int(30) NOT NULL
)"""

joinChannel = """CREATE TABLE joinChannel(
        userId int(15) NOT NULL,
        channelId int(15) NOT NULL
)"""

playlist = """CREATE TABLE playlist(
         playlistId int(15) NOT NULL AUTO_INCREMENT,
         playlistName varchar(30) NOT NULL,
         userId int(15) NOT NULL,
         PRIMARY KEY (playlistId)
)"""

playlist_video = """CREATE TABLE playlist_video(
         playlistId int(15) NOT NULL,
         videoId int(15) NOT NULL
)"""

insert_video = """INSERT INTO `video` (`videoId`, `videoName`,`StorageId`, `vCaption`, `time`, `date`, `thumbnail`, `views`, `likes`, `dislikes`) VALUES
(1, 'video 1','1' , 'video1', '30', '11/6/2020', NULL, 0, 0, 0),
(2, 'video 2', '2', 'video2', '32', '11/6/2020', NULL, 0, 0, 0),
(3, 'video 3', '3','video3', '35', '11/6/2020', NULL, 0, 0, 0);
"""
insert_user = """INSERT INTO `user` (`username`, `userId`, `pass`, `email`, `date`, `profileImage`) VALUES
('mahdi', 1, '3627909a29c3138', 'mahdi@gmail.com', '1625264703.4390085', NULL),
('mobina', 2, '3627909a29c3138', 'mobina@gmail.com', '1625264729.4497058', NULL);
"""
insert_pl = """
INSERT INTO `playlist` (`playlistId`, `playlistName`, `userId`) VALUES
(1, 'watch later', 1),
(2, 'watch later', 2);
"""

cursor.execute(user)
cursor.execute(video)
cursor.execute(channel)
cursor.execute(shareChannel)
cursor.execute(view)
cursor.execute(likes)
cursor.execute(dislikes)
cursor.execute(joinChannel)
cursor.execute(playlist)
cursor.execute(playlist_video)
cursor.execute(insert_video)
cursor.execute(insert_user)
cursor.execute(insert_pl)
connection.close()
