import mysql.connector
from database_constants import DATABASE_NAME, MESSAGES
from data_classes import Relationship, Identity
from status_codes import Status

database = None
cursor = None

class Database_Handler():
    def __init__(self, hostname = None, username = None, password = None):

        global database
        global cursor

        if database is None:
            print("Establishing initial connection with database.")
            database = mysql.connector.connect(host=hostname, user=username, passwd=password)
            print("Connection to database established.")
            database.autocommit = True
            cursor = database.cursor()
            try:
                cursor.execute(f"USE {DATABASE_NAME}")
            except:
                print("Well, that's okay.")

    def add_to_database(self, message):
        print("Adding message to database")
        cursor.execute(f'INSERT INTO {MESSAGES}(message) VALUES("{message}")')
    
    def completely_reset_database(self) -> Status:
        cursor.execute(f'DROP DATABASE {DATABASE_NAME}')
        cursor.execute(f'CREATE DATABASE {DATABASE_NAME}')
        cursor.execute(f'USE {DATABASE_NAME}')
        cursor.execute(f'CREATE TABLE {MESSAGES}(message_id int not null auto_increment primary key, user_id varchar(255) not null, message varchar(255) not null)')
        print("Database completely reset.")
        return Status.OK

    def get_recent_from_table(self, table_name, primary_key) -> list:
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY {primary_key} DESC LIMIT 10')
        return cursor.fetchall()

    def add_message(self, message, user_id) -> Status:
        print("Inserting message.")
        cursor.execute(f'INSERT INTO {MESSAGES}(message, user_id) VALUES("{message}", "{user_id}")')
        print("Message inserted.")
        return Status.OK

    def add_relationship(self, relationship: Relationship) -> Status:
        print(f"Adding relationship where {relationship.dominant} is the dominant to the database.")
        return Status.Ok