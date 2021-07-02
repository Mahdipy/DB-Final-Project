import pymysql
import time
import hashlib, uuid


# database connection


class Main:
    def __init__(self):
        self.connection = pymysql.connect(host="localhost", user="root", passwd="", database="youtube")
        self.cursor = self.connection.cursor()

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
                print('Username is already taken!')
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

    def main(self):
        x = input('Welcome!\n1)Login\n2)Sign Up\n')
        if x == '1':
            self.login()
        elif x == '2':
            self.signup()

    def login(self):
        name = input('Username: ')
        password = input('Password: ')
        hashed_password = hashlib.sha512((password).encode('utf-8')).hexdigest()
        sql = "SELECT * FROM `user` WHERE `username`=%s and `pass`=%s"
        self.cursor.execute(sql, (name, hashed_password[:15]))
        result = self.cursor.fetchone()
        if result:
            print(f'Welcome {name}!')
            while True:
                z = input('enter your code: ')


x = Main()
x.main()
