import mysql.connector
from database_constants import DATABASE_NAME, MESSAGES

class Database_Handler():
    def __init__(self, hostname, username, password, default_database = None):
        print("Establishing connection with database.")
        self.database = mysql.connector.connect(host=hostname, user=username, passwd=password)
        print("Connection established.")
        self.database.autocommit = True
        self.cursor = self.database.cursor()
        try:
            self.cursor.execute(f"USE {DATABASE_NAME}")
        except:
            print("That's okay")

    def add_to_database(self, message):
        print("Adding message to database")
        self.cursor.execute(f'INSERT INTO {MESSAGES}(message) VALUES("{message}")')
    
    def completely_reset_database(self) -> bool:
        self.cursor.execute(f'DROP DATABASE {DATABASE_NAME}')
        self.cursor.execute(f'CREATE DATABASE {DATABASE_NAME}')
        self.cursor.execute(f'USE {DATABASE_NAME}')
        self.cursor.execute(f'CREATE TABLE {MESSAGES}(message_id int not null auto_increment primary key, user_id varchar(255) not null, message varchar(255) not null)')
        print("Database completely reset.")
        return True

    def get_all_from_table(self, table_name) -> list:
        self.cursor.execute(f'SELECT * FROM {table_name} ORDER BY message_id DESC LIMIT 10')
        return self.cursor.fetchall()

    def add_message(self, message, user_id) -> bool:
        print("Inserting message.")
        self.cursor.execute(f'INSERT INTO {MESSAGES}(message, user_id) VALUES("{message}, {user_id}")')
        print("Message inserted.")
        return True