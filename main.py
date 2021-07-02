import pymysql
#database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="youtube")
cursor = connection.cursor()

def signup():
    with connection:
        username = ''
        pas = ''
        email = ''

        while (username == ''):
            username = input("Enter user name")
            # cursor.execute("SELECT username FROM user")
            # result = cursor.fetchone()
            # while (result):
            #     if result == username:
            #         input("Enter another user name")
            #     result = cursor.fetchone()

        while pas == '':
           pas = input("Enter password")

        while pas == '':
          email = input("Enter email")



        cursor.execute("INSERT INTO user (username, pass, email) VALUES (%s, %s, %s)", (username, pas, email))

        connection.commit()

# def login():


signup()