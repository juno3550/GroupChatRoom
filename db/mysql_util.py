import pymysql


class MysqlTool:

    def __init__(self, host, port, db, user, passwd, charset="utf8"):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset

    # 创建数据库连接与执行对象
    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port,
                                        db=self.db, user=self.user, passwd=self.passwd, charset=self.charset)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    # 关闭数据库连接与执行对象
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(e)

    # 获取一行数据
    def get_one(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
        else:
            return result

    # 获取全部行的数据
    def get_all(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)
        else:
            return result

    # 增删改查的私有方法
    def __edit(self, sql):
        try:
            execute_count = self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        else:
            return execute_count

    # 插入数据
    def insert(self, sql):
        return self.__edit(sql)

    # 删除数据
    def delete(self, sql):
        return self.__edit(sql)


if __name__ == "__main__":
    mysql = MysqlTool("localhost", 3306, "test", "root", "admin")
    mysql.connect()
    mysql.insert('insert into user(username, password, nickname) values("username_test1", "pwd_test1", "nick_test1");')
    print(mysql.get_all("select * from user;"))
    mysql.delete('delete from user where username="%s"' % "username_test1")
    print(mysql.get_all("select * from user;"))
