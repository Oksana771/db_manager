import mysql.connector
from prettytable import PrettyTable

if __name__ == '__main__':
    db_manager


class db_manager:
    def __init__(self, host, user, password):
        self.__db = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("CREATE DATABASE IF NOT EXISTS pylogin")
        self.__cursor.execute("USE pylogin")
        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(64), email VARCHAR(128), password VARCHAR(2048))")

    def menu(self):
        exit = False
        while not exit:
            choice = int(input(
                "1. Register\n2. Login\n3. Edit\n4. Delete\n5. Show all users\n6. Search by name\n0 Exit"))
            if choice == 1:
                answer = self.__register()
                print(answer)
            elif choice == 2:
                answer = self.__login()
                print(answer)
            elif choice == 3:
                answer = self.__edit()
                print(answer)
            elif choice == 4:
                answer = self.__delete()
                print(answer)
            elif choice == 5:
                answer = self.__show_all_users()
                print(answer)
            elif choice == 6:
                answer = self.__serch_by_name()
                print(answer)
            elif choice == 0:
                exit = True
                print("Bye!")
            else:
                print("Error!!!")

    def __register(self):
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        confirm_password = input("Confirm password: ")

        if password != confirm_password:
            return "Password do not match."

        self.__cursor.execute(
            "SELECT email FROM users WHERE email = '" + email + "'")
        result = self.__cursor.fetchone()

        if result != None:
            return "Users exists"

        else:
            sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            val = (username, email, password)
            self.__cursor.execute(sql, val)
            self.__db.commit()
            return "User successfully created"

    def __login(self):
        login = input("Login: ")
        password_login = input("Password: ")

        self.__cursor.execute(
            "SELECT password, email FROM users WHERE password = '" + password_login + "' AND email = '" + login + "' ")
        result = self.__cursor.fetchone()

        if result != None:
            return "Welcome!!!!!"
        else:
            return "Password or Login do not match."

    def __edit(self):
        login = input("Login: ")
        password = input("Password: ")

        self.__cursor.execute(
            "SELECT username, email, password FROM users WHERE email = '" + login + "' AND password = '" + password + "' ")
        result = self.__cursor.fetchone()
        if result != None:
            print(login + " Enter new account data: ")
            username = input("New Username: ")
            new_email = input("New Email: ")
            password = input("New Password: ")
            self.__cursor.execute(
                "UPDATE users SET username = '" + username + "', email = '" + new_email + "', password = '" + password + "' WHERE email ='" + login + "'")
            self.__db.commit()
            return username + " your data successfully edited!"
        else:
            return "Password or Login do not match."

    def __delete(self):
        login = input("Login: ")
        password = input("Password: ")

        self.__cursor.execute(
            "SELECT  email, password FROM users WHERE email = '" + login + "' AND password = '" + password + "' ")
        result = self.__cursor.fetchone()
        if result != None:
            self.__cursor.execute(
                "DELETE FROM users WHERE email = '" + login + "'")
            self.__db.commit()
            return login + " your data successfully deleted!"
        else:
            return "Password or Login do not match."

    def __show_all_users(self):
        self.__cursor.execute(
            "SELECT id, username,  email  FROM users")
        result = self.__cursor.fetchall()
        if result != None:
            table = PrettyTable()
            table.field_names = ["id", "username", "email"]
            for id, username, email in result:
                table.add_row([id, username, email])
            print(table)
        else:
            return "No data found!!"
    def __serch_by_name(self):
        email = input("Enter username: ")
        self.__cursor.execute(
            "SELECT id, username,  email  FROM users WHERE email = '" + email + "' ")
        result = self.__cursor.fetchall()
        if result != None:
            find = False
            table = PrettyTable()
            table.field_names = ["id", "username", "email"]
            for id, username, email in result:
                if username == username.capitalize():
                    table.add_row([id, username, email])
                print(table)
                find = True
                break
            if not find:
                print("Name is not defined!!!")