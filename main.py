import pymysql
import time
import hashlib, uuid
import Video
import Print
from termcolor import colored


class Main:
    def __init__(self):
        self.connection = pymysql.connect(host="localhost", user="root", passwd="", database="youtube")
        self.cursor = self.connection.cursor()
        self.userId = 0

    def signup(self):
        username = ''
        pas = ''
        email = ''
        z = True
        while (username == '') | z:
            username = input("Enter Username: ")
            self.cursor.execute("SELECT `username` FROM `user` where `username`=%s", (username,))
            result = self.cursor.fetchone()
            if result:
                Print.print_error('Username Is Already Taken!')
            else:
                break

        while pas == '':
            pas = input("Enter Password: ")

        while email == '':
            email = input("Enter Email: ")
        hashed_password = hashlib.sha512((pas).encode('utf-8')).hexdigest()
        self.cursor.execute("INSERT INTO `user` (`username`, `pass`, `email`, `date`) VALUES (%s, %s, %s, %s)",
                            (username, hashed_password[:15], email, time.time()))
        self.connection.commit()
        sql = "SELECT * FROM `user` WHERE `username`=%s"
        self.cursor.execute(sql, (username,))
        result = self.cursor.fetchone()
        self.userId = result[1]
        self.cursor.execute("INSERT INTO `playlist` (`playlistName`, `userId`) VALUES (%s, %s)",
                            ('watch later', self.userId))
        self.connection.commit()
        print(colored(f'--------------------\nHello {str.capitalize(result[0])}!\n--------------------', 'blue'))
        m = Video.Video(self.userId)
        m.main()

    def main(self):
        x = input('--------------------------\n         Welcome!\n--------------------------\n1)Login\n2)Sign Up\n')
        if x == '1':
            self.login()
        elif x == '2':
            self.signup()

    def login(self):
        while True:
            name = input('Username: ')
            password = input('Password: ')
            hashed_password = hashlib.sha512((password).encode('utf-8')).hexdigest()
            sql = "SELECT * FROM `user` WHERE `username`=%s and `pass`=%s"
            self.cursor.execute(sql, (name, hashed_password[:15]))
            result = self.cursor.fetchone()
            if result:
                print(colored(f'--------------------\nHello {str.capitalize(name)}!\n--------------------', 'blue'))
                self.userId = result[1]
                m = Video.Video(self.userId)
                m.main()
                break
            else:
                Print.print_error('Wrong Username Or Password')


x = Main()
x.main()
