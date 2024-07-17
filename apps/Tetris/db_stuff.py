import sqlite3
from sqlite3 import Error
import os
import random
class Database:
    def __init__(self):
        need_to_create_table = False
        if not os.path.exists('apps/Tetris/Highscores'):
            os.mkdir("Highscores")
            need_to_create_table = True

        self.creatConnection()
        self.cursor = self.conn.cursor()
        if need_to_create_table:
            sql = """
                CREATE TABLE HIGHSCORES (
                    name TEXT,
                    score INTEGER,
                    lines_cleared INTEGER,
                    level INTEGER
                )
            """
            self.cursor.execute(sql)
            self.conn.commit()


    def creatConnection(self):
        try:
            self.conn = sqlite3.connect('apps/Tetris/Highscores/Highscores.db')
        except Error as e:
            print(e)

    def insert_score(self, name, score, level, lines_cleared):

        self.cursor.execute(f'INSERT INTO HIGHSCORES (name, score, level, lines_cleared) VALUES(?,?,?,?)', (name, score,lines_cleared, level, ))
        self.conn.commit()

    def FetchAll(self):
        self.cursor.execute('SELECT * FROM HIGHSCORES')
        return self.cursor.fetchall()
#
# A = Database()
#
# for x in range(1000):
#     A.insert_score('HFJKSkjlha', random.randint(400, 999999), random.randint(10, 600), random.randint(0, 32))