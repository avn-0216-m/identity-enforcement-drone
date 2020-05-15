import mysql.connector
from database_constants import DATABASE_NAME, MESSAGES, get_migration, RELATIONSHIPS
from data_classes import Relationship, Identity, Status, Response
from notable_entities import ENFORCEMENT_DRONE
from default_identities import init_default_identities_for_guild
from rowmapper import result_to_identity, result_to_relationship, result_to_user

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
            cursor = database.cursor(buffered=True, dictionary=True)
            try:
                cursor.execute(f"USE {DATABASE_NAME}")
            except:
                print("Well, that's okay.")

    #Admin
    def completely_reset_database(self) -> Status:
        print("Completely resetting database.")
        for step in get_migration():
            current_step = step
            print("EXECUTING: " + current_step)
            cursor.execute(current_step)
        print("Database completely reset.")
        return Status.OK

    #General
    def get_recent_from_table(self, table_name, key, amount) -> list:
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY {key} DESC LIMIT {amount}')
        return cursor.fetchall()

    def get_all_from_table(self, table_name: str) -> Response:
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
        return Response(Status.OK, data)

    def get_all_matches_from_table(self, table_name: str, key, value) -> Response:
        cursor.execute(f'SELECT * FROM {table_name} WHERE {key} = {value}')
        data = cursor.fetchall()
        return Response(Status.OK, data)

    #Messages
    def add_message(self, message, user_id) -> Status:
        print("Inserting message.")
        cursor.execute(f'INSERT INTO {MESSAGES}(message_content, user_id) VALUES("{message}", "{user_id}")')
        print("Message inserted.")
        return Status.OK
    
    #Relationship Queries
    def find_potential_relationship(self, dom_id, sub_id) -> Response: #List of relationships
        print("Checking if there's a prexisting relationship for the BDSM request.")
        cursor.execute(f'SELECT * FROM {RELATIONSHIPS} WHERE dominant_id = {dom_id} AND submissive_id = {sub_id};')
        data = cursor.fetchall()
        return Response(Status.OK, result_to_relationship(data))

    def find_confirmed_relationship(self, dom_id, sub_id) -> Response:
        cursor.execute(f'SELECT relationship_id FROM relationships WHERE dominant_id = {dom_id} AND submissive_id = {sub_id} AND pending = 0')
        data = cursor.fetchall()
        return Response(Status.OK, result_to_relationship(data))

    def confirm_relationship(self, relationship_id) -> Status:
        cursor.execute(f'UPDATE relationships SET pending = 0 WHERE relationship_id = {relationship_id}')
        return Status.OK

    def get_number_of_submissives(self, dom_id) -> int:
        print("Getting number of subs.")
        cursor.execute(f'SELECT relationship_id FROM {RELATIONSHIPS} WHERE dominant_id = {dom_id};')
        data = cursor.fetchall()
        return len(data)

    def add_relationship(self, relationship: Relationship) -> Status:
        cursor.execute(f'INSERT INTO {RELATIONSHIPS}(dominant_id, submissive_id, initiated_by, pending) VALUES("{relationship.dominant_id}","{relationship.submissive_id}","{relationship.initiated_by}","{relationship.pending}");')
        return Status.OK

    def get_all_submissives(self, dom_id: int) -> list:
        cursor.execute(f'SELECT submissive_id FROM {RELATIONSHIPS} WHERE dominant_id = {dom_id} AND pending = 0;')
        data = cursor.fetchall()
        return Response(Status.OK, result_to_relationship(data))

    #Identities
    def refresh_default_identities(self, guild_id):
        #Delete all identities for given guild belonging to the enforcement drone.
        cursor.execute(f'DELETE FROM identities WHERE owner_id = {guild_id} AND owner_type = "guild";')
        #Reinsert the default identities.
        for statement in init_default_identities_for_guild(guild_id):
            print(f"EXECUTING: {statement}")
            cursor.execute(statement)

    def get_identity_by_role(self, role_name, guild_id) -> Identity:
        cursor.execute(f'SELECT * FROM identities WHERE name = {role_name} AND owner_id = {guild_id} AND owner_type = "guild";')
        data = cursor.fetchall()
        return Response(Status.OK, result_to_identity(data))

    def get_all_identities_for_guild(self, guild_id) -> Identity:
        cursor.execute(f'SELECT name, display_name FROM identities WHERE owner_id = {guild_id} AND owner_type = "guild";')
        data = cursor.fetchall()
        return Response(Status.OK, result_to_identity(data))

    def get_all_identities_for_user(self, user_id) -> Identity:
        cursor.execute(f'SELECT name FROM identities WHERE owner_id = {user_id} AND owner_type = "user";')
        data = cursor.fetchall()
        return Response(Status.OK, result_to_identity(data))

    #Users
    def get_registered_user(self, user_id):
        cursor.execute(f'SELECT user_id FROM users WHERE user_id = {user_id}')
        data = cursor.fetchall()
        return Response(Status.OK, result_to_user(data))
    
    def register_user_with_id(self, user_id, drone_id):
        cursor.execute(f'INSERT INTO users(user_id, drone_id) VALUES({user_id}, LPAD({drone_id}, 4, 0));')
        return Status.OK

    def register_user(self, user_id):
        cursor.execute(f'INSERT INTO users(user_id) VALUES({user_id});')
        return Status.OK

    def get_all_registered_drones(self):
        cursor.execute('SELECT drone_id FROM users')
        data = cursor.fetchall()
        return Response(Status.OK, result_to_user(data))