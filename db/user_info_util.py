from db import mysql_util

class UserUtil:

    def __init__(self, host, port, db, user, passwd, charset="utf8"):
        self.mysql = mysql_util.MysqlTool(host, port, db, user, passwd, charset)

    def user_check(self, username):
        check_sql = "SELECT username,password,nickname FROM user WHERE username = '%s'" % username
        self.mysql.connect()
        user_info = self.mysql.get_all(check_sql)
        self.mysql.close()
        return user_info

    def user_insert(self, username, passwd, nickname):
        insert_sql = "INSERT INTO user(username,password,nickname) VALUES('%s','%s','%s')" % (username, passwd, nickname)
        self.mysql.connect()
        self.mysql.insert(insert_sql)
        self.mysql.close()

user_util = UserUtil("localhost", 3306, "test", "root", "admin")

if __name__ == "__main__":
    print(user_util.user_check("username_test"))
    user_util.user_insert("username_test2", "pwd", "nickname")
    print(user_util.user_check("username_test2"))
