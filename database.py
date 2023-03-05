import sqlite3  #imports entire Library. Use: sqlite3.XXXX
from sqlite3 import Error  # imports a  member in our namespace. Usa directly
from constants import *


class DatabaseSqlite():

    def __init__(self, path="mydatabase.sqlite"):
        self.connection = self.create_connection(path)
        # Create Table
        self.execute_query("CREATE TABLE IF NOT EXISTS highscores (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,score INTEGER,time INTEGER,multiplayer INTEGER);")

    def create_connection(self, path):
        connection = None
        try:
            # Create Connection
            connection = sqlite3.connect(path)  #create or use existing
            print("Connection to SQLite succesful")
        except Error as e:
            print(f"The error '{e}' occured")
        return connection

    def execute_query(self, query) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print(f"Query [{query}] executed successfully")
            return True
        except Error as e:
            print(f"The error '{e}' occured")
            return False

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()  # to fetch as tuples the results
            column_names = [
                description[0] for description in cursor.description
            ]
            return column_names, result
        except Error as e:
            print(f"The error '{e}' occured")
            return result

    def read_all_highscores(self):
        # Select DATA
        select_highscores = "SELECT * from highscores ORDER BY score DESC;"
        return self.execute_read_query(select_highscores)

    def read_all_highscoresByType(self, multiplayer: bool, limit=10):
        # Select DATA
        select_highscores_by_type = f'SELECT name,score,time from highscores WHERE multiplayer={multiplayer} ORDER BY score DESC LIMIT {limit};'
        return self.execute_read_query(select_highscores_by_type)

    def create_highscore(self, name: str, score: int, time: int,
                         mutliplayer: bool) -> bool:
        # Insert DATA
        create_highscore = f"INSERT INTO highscores(name,score,time,multiplayer) values ('{name}',{score},{time},{mutliplayer});"
        return self.execute_query(create_highscore)

    def clear_highscores(self) -> bool:
        delete_all = "DELETE FROM highscores"
        return self.execute_query(delete_all)
