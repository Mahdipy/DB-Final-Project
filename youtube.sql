DROP database IF EXISTS youtube;

create database youtube ;
use youtube;

DROP TABLE IF EXISTS youtube.user;
CREATE TABLE youtube.user (
                            username varchar(30)  NOT NULL,
                            userId int(15) NOT NULL AUTO_INCREMENT,
                            pass varchar(15)  NOT NULL,
                            email varchar(30)  NOT NULL,
                            date varchar(30)  NOT NULL,
                            profileImage varchar(30),
                            PRIMARY KEY (userId)
);

DROP TABLE IF EXISTS youtube.video;
CREATE TABLE youtube.video (
                            videoId int(15) NOT NULL AUTO_INCREMENT,
                            videoName varchar(30)  NOT NULL,
                            vCaption text(50) NOT NULL,
                            time varchar(30)  NOT NULL,
                            data varchar(30)  NOT NULL,
                            thumbnail varchar(30),
                            views int(15) NOT NULL,
                            likes int(15) NOT NULL,
                            PRIMARY KEY (videoId)
);

DROP TABLE IF EXISTS youtube.channel;
CREATE TABLE youtube.channel (
    channelId   int(15) NOT NULL AUTO_INCREMENT,
    userId      int(15) NOT NULL,
    channelName varchar(30) NOT NULL,
    date        varchar(30) NOT NULL,
    chCaption   text(50) NOT NULL,
    PRIMARY KEY (channelId)
);

DROP TABLE IF EXISTS youtube.shareChannel;
CREATE TABLE youtube.shareChannel(
     userId  int(15) NOT NULL,
     videoId int(15) NOT NULL,
     channelId int(15) NOT NULL
);

DROP TABLE IF EXISTS youtube.view;
CREATE TABLE youtube.view(
     userId  int(15) NOT NULL,
     videoId int(15) NOT NULL
);

DROP TABLE IF EXISTS youtube.comment;
CREATE TABLE youtube.comment (
       userId int(15) NOT NULL,
       videoId int(30) NOT NULL,
       comment text(50) NOT NULL,
       commentId int(15) NOT NULL

);

DROP TABLE IF EXISTS youtube.likes;
CREATE TABLE youtube.likes (
     userId int(15) NOT NULL,
     videoId int(30) NOT NULL
);

DROP TABLE IF EXISTS youtube.joinChannel;
CREATE TABLE youtube.joinChannel(
        userId int(15) NOT NULL,
        channelId int(15) NOT NULL
);

DROP TABLE IF EXISTS youtube.playlist;
CREATE TABLE youtube.playlist(
         userId int(15) NOT NULL,
         videoId int(30) NOT NULL,
         playlistId int(15) NOT NULL,
         playlistName varchar(30) NOT NULL
);
