import pymysql
import Print
from termcolor import colored


class Video:
    def __init__(self, userId):
        self.connection = pymysql.connect(host="localhost", user="root", passwd="", database="youtube")
        self.cursor = self.connection.cursor()
        self.userId = userId
        self.videoId = None

    def main(self):
        while True:
            line = input('>> ')
            if line == 'new playlist':
                self.new_playlist()
            if line == 'exit':
                Print.print_success('Good Bye!')
                exit()
            # if line == 'add':
            #     self.add_video_to_playlist()
            if line == 'videos':
                self.video_list()

    def new_playlist(self):
        name = input('Name: ')
        self.cursor.execute("INSERT INTO `playlist` (`playlistName`, `userId`) VALUES (%s, %s)",
                            (name, self.userId))

        self.connection.commit()
        Print.print_success('PlayList Added Successfully')

    def add_video_to_playlist(self, videoId):
        self.cursor.execute("SELECT * from `playlist` where `userId`=%s",
                            (self.userId,))
        result = self.cursor.fetchone()
        i = 1
        playlisttId = []
        print('-------------------------\n       PlayLists\n-------------------------')
        print('0: Back')
        while result:
            print(f'{i}: {result[1]}')
            i += 1
            playlisttId.append(result[0])
            result = self.cursor.fetchone()
        print(f'{i}: New PlayList')
        index = int(input()) - 1
        if index == -1: return
        if index == (i-1):
            self.new_playlist()
            return
        self.cursor.execute("INSERT INTO `playlist_video` (`playlistId`, `videoId`) VALUES (%s, %s)",
                            (playlisttId[index], videoId))

        self.connection.commit()
        Print.print_success('Video Added To Playlist Successfully')

    def video_list(self):
        self.cursor.execute("SELECT * from `video`")
        result = self.cursor.fetchone()
        print('----------------------------\n          Videos\n----------------------------')
        print('0: Back')
        video_id = []
        while result:
            print(f'{result[0]}: {result[1]}')
            video_id.append(result[0])
            result = self.cursor.fetchone()
        index = int(input()) - 1
        if index == -1:
            return
        self.cursor.execute("SELECT * from `video` where `videoId`=%s", (video_id[index]))
        result = self.cursor.fetchone()
        views = int(result[6]) + 1
        self.cursor.execute("UPDATE `video` SET `views` = %s WHERE `videoId` = %s", (views, video_id[index]))
        self.connection.commit()
        self.cursor.execute("INSERT INTO `view` (`userId`, `videoId`) VALUES (%s, %s)",
                            (self.userId, video_id[index]))
        self.connection.commit()
        while True:
            print(f'------------------------------\n           {result[1]}\n------------------------------')
            x = input('0: Back\n1: Like\n2: Dislike\n3: Comments\n4: Add to my playlist\n')
            if x == '0':
                self.video_list()
                break
            if x == '1':
                self.add_like(video_id[index])
            if x == '2':
                self.add_dislike(video_id[index])
            if x == '4':
                self.add_video_to_playlist(video_id[index])

    def add_like(self, video_id):
        self.cursor.execute("SELECT * from `likes` where `videoId`=%s and `userId`=%s", (video_id, self.userId))
        is_liked = self.cursor.fetchone()
        self.cursor.execute("SELECT * from `video` where `videoId`=%s", (video_id,))
        result = self.cursor.fetchone()
        if not is_liked:
            likes = int(result[7]) + 1
            self.cursor.execute("INSERT INTO `likes` (`userId`, `videoId`) VALUES (%s, %s)",
                                (self.userId, video_id))
            self.connection.commit()
            print(colored('like added...', 'green'))
        else:
            likes = int(result[7]) - 1
            self.cursor.execute("DELETE from `likes` where `userId`=%s and `videoId`=%s", (self.userId, video_id))
            self.connection.commit()
            print(colored('like removed...', 'red'))

        self.cursor.execute("UPDATE `video` SET `likes` = %s WHERE `videoId` = %s", (likes, video_id))
        self.connection.commit()

    def add_dislike(self, video_id):
        self.cursor.execute("SELECT * from `dislikes` where `videoId`=%s and `userId`=%s", (video_id, self.userId))
        is_disliked = self.cursor.fetchone()
        self.cursor.execute("SELECT * from `video` where `videoId`=%s", (video_id,))
        result = self.cursor.fetchone()
        if not is_disliked:
            dislikes = int(result[8]) + 1
            self.cursor.execute("INSERT INTO `dislikes` (`userId`, `videoId`) VALUES (%s, %s)",
                                (self.userId, video_id))
            self.connection.commit()
            print(colored('dislike added...', 'green'))
        else:
            dislikes = int(result[8]) - 1
            self.cursor.execute("DELETE from `dislikes` where `userId`=%s and `videoId`=%s", (self.userId, video_id))
            self.connection.commit()
            print(colored('dislike removed...', 'red'))

        self.cursor.execute("UPDATE `video` SET `dislikes` = %s WHERE `videoId` = %s", (dislikes, video_id))
        self.connection.commit()
