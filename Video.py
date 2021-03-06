import pymysql
import Print
from termcolor import colored
import random
import datetime


class Video:
    def __init__(self, userId):
        self.connection = pymysql.connect(host="localhost", user="root", passwd="", database="youtube")
        self.cursor = self.connection.cursor()
        self.userId = userId
        self.videoId = None

    def main(self):
        while True:
            line = input('>> ')
            if line == '--help':
                print('-----------------------------------------\n'
                      '                Commands\n'
                      '-----------------------------------------\n'
                      'new playlist:       Create New PlayList\n'
                      'my playlist:        View User\'s PlayList\n'
                      'videos:             View Videos\n'
                      'channels:           View Channels\n'
                      'new channel:        Create New Channel\n'
                      'upload:             Upload New Video\n'
                      'search              Search\n'
                      'exit:               Exit\n'
                      '-----------------------------------------')
            elif line == 'new playlist':
                self.new_playlist()
            elif line == 'my playlists':
                self.playlistmenu()
            elif line == 'exit':
                Print.print_success('Good Bye!')
                exit()
            elif line == 'videos':
                self.video_list(2, None, None)
            elif line == 'upload':
                self.upload()
            elif line == 'new channel':
                self.new_channel()
            elif line == 'channels':
                self.channels()
            elif line == 'search':
                self.search()
            else:
                Print.print_error('Command Not Found (--help for command\'s list)')

    # -------------------------------------playlist-----------------------------------------------------------
    def playlists(self):
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
        if index == (i - 1):
            self.new_playlist()
            return
        return playlisttId[index]
        # self.view_playlist(playlisttId[index])

    def playlistmenu(self):
        x = self.playlists()
        self.view_playlist(x)

    def view_playlist(self, playlist_id):
        sql = "SELECT * FROM `playlist` where `playlistId`=%s"
        self.cursor.execute(sql, (playlist_id,))
        result = self.cursor.fetchone()
        while True:
            print(f'--------------------------------------------------\n'
                  f'{result[1]}\n'
                  f'--------------------------------------------------\n'
                  f'0: Back\n1: Videos\n2: Remove Videos\n3: Remove PlayList'
                  )
            x = input()
            if x == '0':
                return
            elif x == '1':
                self.video_list(0, playlist_id, None)
            elif x == '2':
                self.remove_video(playlist_id)
            elif x == '3':
                self.remove_playlist(playlist_id)
                return

    def remove_video(self, playlist_id):
        self.cursor.execute(
            "SELECT * from `video`, `playlist_video`  where `playlist_video`.`playlistId`= %s and `playlist_video`.`videoId`=`video`.`videoId`",
            (playlist_id,))
        res = self.cursor.fetchone()
        print('----------------------------\n          Videos\n----------------------------')
        print('0: Back')
        video_id = []
        while res:
            print(f'{res[0]}: {res[1]}')
            video_id.append(res[0])
            res = self.cursor.fetchone()
        index = int(input()) - 1
        if index == -1:
            return
        self.cursor.execute("DELETE FROM `playlist_video` WHERE `videoId`=%s and `playlistId`=%s",
                            (video_id[index], playlist_id))

    def remove_playlist(self, playlist_id):
        self.cursor.execute("DELETE FROM `playlist` WHERE `playlistId`=%s", (playlist_id,))

    def new_playlist(self):
        name = input('Name: ')
        self.cursor.execute("INSERT INTO `playlist` (`playlistName`, `userId`) VALUES (%s, %s)",
                            (name, self.userId))

        self.connection.commit()
        Print.print_success('PlayList Added Successfully')

    def add_video_to_playlist(self, videoId):
        playlistId = self.playlists()
        self.cursor.execute("INSERT INTO `playlist_video` (`playlistId`, `videoId`) VALUES (%s, %s)",
                            (playlistId, videoId))
        self.connection.commit()
        Print.print_success('Video Added To Playlist Successfully')

    # ------------------------------------video-------------------------------------------------
    def video_list(self, channel_playlist_flag, playlist_id, channel_id):
        if channel_playlist_flag == 0:
            self.cursor.execute(
                "SELECT * from `video`, `playlist_video`  where `playlist_video`.`playlistId`= %s and `playlist_video`.`videoId`=`video`.`videoId`",
                (playlist_id,))
        elif channel_playlist_flag == 1:
            self.cursor.execute(
                "SELECT * from `video`, `shareChannel`  where `shareChannel`.`channelId`= %s and `shareChannel`.`videoId`=`video`.`videoId`",
                (channel_id,))
        else:
            self.cursor.execute("SELECT * from `video`")
        result = self.cursor.fetchone()
        print('----------------------------\n          Videos\n----------------------------')
        print('0: Back')
        video_id = []
        i = 1
        while result:
            print(f'{i}: {result[1]}')
            i += 1
            video_id.append(result[0])
            result = self.cursor.fetchone()
        index = int(input()) - 1
        if index == -1:
            return
        self.cursor.execute("SELECT * from `video` where `videoId`=%s", (video_id[index]))
        result = self.cursor.fetchone()
        views = int(result[7]) + 1
        self.cursor.execute("UPDATE `video` SET `views` = %s WHERE `videoId` = %s", (views, video_id[index]))
        self.connection.commit()
        self.cursor.execute("INSERT INTO `view` (`userId`, `videoId`) VALUES (%s, %s)",
                            (self.userId, video_id[index]))
        self.connection.commit()
        while True:
            print(f'------------------------------\n           {result[1]}\n------------------------------')
            x = input('0: Back\n1: Like\n2: Dislike\n3: Comments\n4: Add to my playlist\n')
            if x == '0':
                return
            if x == '1':
                self.add_like(video_id[index])
            if x == '2':
                self.add_dislike(video_id[index])
            if x == '3':
                self.showComment(video_id[index])
            if x == '4':
                self.add_video_to_playlist(video_id[index])

    def add_like(self, video_id):
        self.cursor.execute("SELECT * from `likes` where `videoId`=%s and `userId`=%s", (video_id, self.userId))
        is_liked = self.cursor.fetchone()
        self.cursor.execute("SELECT * from `video` where `videoId`=%s", (video_id,))
        result = self.cursor.fetchone()
        if not is_liked:
            likes = int(result[8]) + 1
            self.cursor.execute("INSERT INTO `likes` (`userId`, `videoId`) VALUES (%s, %s)",
                                (self.userId, video_id))
            self.connection.commit()
            print(colored('like added...', 'green'))
        else:
            likes = int(result[8]) - 1
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
            dislikes = int(result[9]) + 1
            self.cursor.execute("INSERT INTO `dislikes` (`userId`, `videoId`) VALUES (%s, %s)",
                                (self.userId, video_id))
            self.connection.commit()
            print(colored('dislike added...', 'green'))
        else:
            dislikes = int(result[9]) - 1
            self.cursor.execute("DELETE from `dislikes` where `userId`=%s and `videoId`=%s", (self.userId, video_id))
            self.connection.commit()
            print(colored('dislike removed...', 'red'))

        self.cursor.execute("UPDATE `video` SET `dislikes` = %s WHERE `videoId` = %s", (dislikes, video_id))
        self.connection.commit()

    def upload(self):
        name = input('Video Name: ')
        video_time = input('Video Time: ')
        caption = input('Video Caption: ')
        thumbnail = input('thumbnail: ')
        storage = name + caption + video_time + str(random.randint(0, 10000))
        self.cursor.execute(
            "INSERT INTO `video` (`videoName`,`StorageId`, `vCaption`, `time`, `date`, `thumbnail`, `views`, `likes`, `dislikes`) VALUES( %s,%s , %s, %s, %s, %s, 0, 0, 0)",
            (name, storage, caption, video_time, datetime.datetime.now(),
             thumbnail))
        self.connection.commit()
        Print.print_success('Video Uploaded Successfully')
        self.cursor.execute("SELECT * from `video` where `StorageId`=%s", (storage,))
        result = self.cursor.fetchone()
        return result

    def showComment(self, videoId):
        self.cursor.execute("SELECT * from `comment` where videoId=%s ", (videoId))
        res = self.cursor.fetchone()
        print('----------------------------\n          Comments\n----------------------------')
        while res:
            print('-----------------------------------------------------------------')
            if res[1] == self.userId:
                print(f'{res[0]}) {res[3]} (you can delete this comment)')
            else:
                print(f'{res[0]}) {res[3]}')
            print('-----------------------------------------------------------------')
            res = self.cursor.fetchone()

        x = input("0: Back \n1: Delete Comment \n2: Add Comment\n")
        if x == '2':
            com = input('Comment: ')
            self.cursor.execute("INSERT INTO `comment` (`userId`, `videoId`, `comment`) VALUES (%s, %s , %s)",
                                (self.userId, videoId, com))
        elif x == '1':
            id = input("Enter index of the commend you want to delete: ")
            self.cursor.execute("DELETE FROM `comment` where `commentId`=%s and `userId`=%s", (id, self.userId))
        self.connection.commit()

    # ---------------------chnnnel------------------------------------------------------------------------------
    def new_channel(self):
        name = input('Channel Name: ')
        caption = input('Channel Caption: ')
        sql = "INSERT INTO `channel` (`userId`, `channelName`, `date`, `chCaption`) VALUES (%s, %s, %s, %s);"
        self.cursor.execute(sql, (self.userId, name, datetime.datetime.now(), caption))
        self.connection.commit()
        Print.print_success('Channel Added Successfully')

    def add_to_channel(self, channel_id):
        re = self.upload()
        sql = "INSERT INTO `shareChannel` (`userId`, `videoId`, `channelId`) VALUES (%s, %s, %s);"
        self.cursor.execute(sql, (self.userId, re[0], channel_id))
        self.connection.commit()

    def remove_from_channel(self, channel_id):
        self.cursor.execute(
            "SELECT * from `video`, `shareChannel`  where `shareChannel`.`channelId`= %s and `shareChannel`.`videoId`=`video`.`videoId`",
            (channel_id,))
        res = self.cursor.fetchone()
        print('----------------------------\n          Videos\n----------------------------')
        print('0: Back')
        video_id = []
        i = 1
        while res:
            print(f'{i}: {res[1]}')
            i += 1
            video_id.append(res[0])
            res = self.cursor.fetchone()
        index = int(input()) - 1
        if index == -1:
            return
        self.cursor.execute("DELETE FROM `shareChannel` WHERE `videoId`=%s and `channelId`=%s",
                            (video_id[index], channel_id))

    def remove_channel(self, channel_id):
        self.cursor.execute(
            'DELETE FROM `video` where `videoId` in (select `videoId` from `shareChannel` where `channelId`=%s)',
            (channel_id,))
        self.connection.commit()
        self.cursor.execute("DELETE FROM `channel` WHERE `channelId`=%s", (channel_id,))
        self.connection.commit()
        self.cursor.execute("DELETE FROM `shareChannel` WHERE `channelId`=%s", (channel_id,))
        self.connection.commit()

    def channels(self):
        sql = "SELECT * FROM `channel`"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        channelId = []
        i = 1
        print('-------------------------\n       Channels\n-------------------------')
        print('0: Back')
        while result:
            print(f'{i}: {result[2]}')
            i += 1
            channelId.append(result[0])
            result = self.cursor.fetchone()
        print(f'{i}: New Channel')
        index = int(input()) - 1
        if index == -1: return
        if index == (i - 1):
            self.new_channel()
            return
        self.view_channel(channelId[index])

    def view_channel(self, channel_id):
        sql = "SELECT * FROM `channel` where `channelId`=%s"
        self.cursor.execute(sql, (channel_id,))
        result = self.cursor.fetchone()
        while True:
            if result[1] == self.userId:
                print(f'--------------------------------------------------\n'
                      f'{result[2]}\n'
                      f'{result[4]}\n'
                      f'--------------------------------------------------\n'
                      f'0: Back\n1: Videos\n2: Add Video\n3: Remove Video\n4: Remove Channel'
                      )
                x = input()
                if x == '0':
                    return
                elif x == '1':
                    self.video_list(1, None, channel_id)
                elif x == '2':
                    self.add_to_channel(channel_id)
                elif x == '3':
                    self.remove_from_channel(channel_id)
                elif x == '4':
                    self.remove_channel(channel_id)
                    return
            else:
                print(f'--------------------------------------------------\n'
                      f'{result[2]}\n'
                      f'{result[4]}\n'
                      f'--------------------------------------------------\n'
                      f'0: Back\n1: Follow\n2: UnFollow\n3: Videos'
                      )
                x = input()
                if x == '0':
                    return
                elif x == '1':
                    self.followChannel(channel_id)
                elif x == '2':
                    self.unfollowChannel(channel_id)
                elif x == '3':
                    self.video_list(1, None, channel_id)

    # follow channel by me
    def followChannel(self, channelId):
        sql = "SELECT * FROM `joinChannel` WHERE `userId` =%s AND `channelId` = %s"
        self.cursor.execute(sql, (self.userId, channelId))
        res = self.cursor.execute(sql, (self.userId, channelId))
        if not res:
            sql = "INSERT INTO `joinChannel` (`userId`, `channelId`) VALUES (%s, %s)"
            self.cursor.execute(sql, (self.userId, channelId))
            self.connection.commit()
            Print.print_success('You Joined This Channel')
        else:
            print(colored('You Already Joined This Channel', 'red'))

    # unFollow channel
    def unfollowChannel(self, channelId):

        sql = "SELECT * FROM `joinChannel` WHERE `userId` =%s AND `channelId` = %s"
        self.cursor.execute(sql, (self.userId, channelId))
        res = self.cursor.execute(sql, (self.userId, channelId))
        if res:
            sql = "DELETE FROM `joinChannel` WHERE `userId`=%s and `channelId`=%s"
            self.cursor.execute(sql, (self.userId, channelId))
            self.connection.commit()
            Print.print_success('You Leave This Channel')
        else:
            print(colored('You are not a member of this channel', 'red'))

    # search added by me
    def search(self):
        print("what are you searching for:")
        x = input('1: video \n2: channel \n3: playlist\n')
        name = input("Enter search word: ")
        if x == '1':
            sql = "SELECT * FROM `video` where `videoName` = %s"
            self.cursor.execute(sql, (name,))
            videoname = self.cursor.fetchone()
            while videoname:
                Print.print_success(f'video id : {videoname[0]} video name : {videoname[1]}')
                videoname = self.cursor.fetchone()

        if x == '2':
            sql = "SELECT * FROM `channel` where `channelName` = %s"
            self.cursor.execute(sql, (name))
            chname = self.cursor.fetchone()
            while chname:
                Print.print_success(f"channel id : {chname[0]} channel name: {chname[2]}")
                chname = self.cursor.fetchone()

        if x == '3':
            sql = "SELECT * FROM `playlist` where `playlistName` = %s"
            self.cursor.execute(sql, (name,))
            pname = self.cursor.fetchone()
            while pname:
                Print.print_success(f"play list id : { pname[0]}  play list name: { pname[2]}")
                pname = self.cursor.fetchone()


