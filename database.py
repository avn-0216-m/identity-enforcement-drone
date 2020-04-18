import mysql.connector
from database_constants import DATABASE_NAME, MESSAGES, MIGRATION, RELATIONSHIPS
from data_classes import Relationship, Identity, Status, Response

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
            cursor = database.cursor(buffered=True)
            try:
                cursor.execute(f"USE {DATABASE_NAME}")
            except:
                print("Well, that's okay.")

    #Admin
    def completely_reset_database(self) -> Status:
        print("Completely resetting database.")
        for step in MIGRATION:
            current_step = step
            cursor.execute(current_step)
        print("Database completely reset.")
        return Status.OK

    #General
    def get_recent_from_table(self, table_name, key, amount) -> list:
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY {key} DESC LIMIT {amount}')
        return cursor.fetchall()

    def get_all_from_table(self, table_name: str, key: str) -> Response:
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
        return Response(Status.OK, data)

    #Messages
    def add_message(self, message, user_id) -> Status:
        print("Inserting message.")
        cursor.execute(f'INSERT INTO {MESSAGES}(message_content, user_id) VALUES("{message}", "{user_id}")')
        print("Message inserted.")
        return Status.OK
    
    #Relationship Queries
    def find_prexisting_relationship(self, dom_id, sub_id, initiated_by) -> bool:
        print("Checking if there's a prexisting relationship for the BDSM request.")
        cursor.execute(f'SELECT * FROM {RELATIONSHIPS} WHERE dominant_id = {dom_id} AND submissive_id = {sub_id} AND initiated_by = {initiated_by};')
        data = cursor.fetchall()
        return len(data) != 0

    def get_number_of_submissives(self, dom_id) -> int:
        print("Getting number of subs.")
        cursor.execute(f'SELECT * FROM {RELATIONSHIPS} WHERE dominant_id = {dom_id};')
        data = cursor.fetchall()
        return len(data)

    def add_relationship(self, relationship: Relationship) -> Status:
        print(f"Adding relationship where {relationship.dominant} is the dominant to the database.")
        cursor.execute(f'INSERT INTO {RELATIONSHIPS}(dominant_id, submissive_id, initiated_by, pending) VALUES("{relationship.dominant}","{relationship.submissive}","{relationship.initiated_by}","{relationship.pending}");')
        return Status.OK

    def get_all_submissives(self, dom_id: int) -> list:
        cursor.execute(f'SELECT submissive_id FROM {RELATIONSHIPS} WHERE dominant_id = {dom_id};')
        return cursor.fetchall()