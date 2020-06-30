import sqlite3
from database_constants import DATABASE_NAME, MESSAGES, get_migration, RELATIONSHIPS
from data_classes import Relationship, Identity, Status, Response
from notable_entities import ENFORCEMENT_DRONE
from default_identities import init_default_identities_for_guild
from rowmapper import result_to_identity, result_to_relationship, result_to_user
import logging
import sys

class Database_Handler():

    database_name = "identity_enforcement_drone.sqlite3"
    connection = None
    cursor = None

    def dict_factory(self, cursor, row):
        self.logger.info("Converting database tuple to dictionary.")
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self):

        self.logger = logging.getLogger("Identity Enforcement Drone")

        if Database_Handler.connection is None:
            #Create a new connection.
            new_connection = sqlite3.connect(Database_Handler.database_name)
            new_connection.row_factory = self.dict_factory
            Database_Handler.connection = new_connection
        self.connection = Database_Handler.connection
        if Database_Handler.cursor is None:
            Database_Handler.cursor = Database_Handler.connection.cursor()
        self.cursor = Database_Handler.cursor

    def migration(self):
        self.cursor.executescript("""
                            CREATE TABLE IF NOT EXISTS Users(
                                user_id INTEGER PRIMARY KEY,
                                drone_id TEXT,
                                safe_words TEXT,
                                bulge INTEGER
                            );

                            CREATE TABLE IF NOT EXISTS Identities(
                                identity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                description TEXT,
                                avatar TEXT,
                                replacement_lexicon TEXT,
                                allowance_lexicon TEXT,
                                display_name TEXT,
                                display_name_with_id TEXT,
                                owner_id INTEGER,
                                color INTEGER,
                                override_chance INTEGER,
                                override_lexicon TEXT,
                                strict INTEGER
                            );

                            CREATE TABLE IF NOT EXISTS Relationships(
                                relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                dominant_id INTEGER NOT NULL,
                                submissive_id INTEGER NOT NULL,
                                initiated_by INTEGER NOT NULL,
                                pending INTEGER NOT NULL
                            );

                            CREATE TABLE IF NOT EXISTS Enforcements(
                                enforcement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                enforced_id INTEGER NOT NULL,
                                server_id INTEGER NOT NULL
                            );

                            """)
        self.connection.commit()

    #General
    def get_recent_from_table(self, table_name, key, amount) -> list:
        self.cursor.execute(f'SELECT * FROM {table_name} ORDER BY {key} DESC LIMIT {amount}')
        return self.cursor.fetchall()

    def get_all_from_table(self, table_name: str) -> Response:
        self.cursor.execute(f'SELECT * FROM {table_name}')
        data = self.cursor.fetchall()
        return Response(Status.OK, data)

    def get_all_matches_from_table(self, table_name: str, key, value) -> Response:
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE {key} = {value}')
        data = self.cursor.fetchall()
        return Response(Status.OK, data)
    
    #Relationship Queries
    def find_potential_relationship(self, dom_id, sub_id) -> Response: #List of relationships
        print("Checking if there's a prexisting relationship for the BDSM request.")
        self.cursor.execute(f'SELECT * FROM {RELATIONSHIPS} WHERE dominant_id = {dom_id} AND submissive_id = {sub_id};')
        data = self.cursor.fetchall()
        return Response(Status.OK, result_to_relationship(data))

    def relationship_already_exists(self, dom_id, sub_id) -> bool:
        self.logger.info(f"Checking if {dom_id} and {sub_id} already have a relationship.")
        self.cursor.execute(f"SELECT * FROM Relationships WHERE dominant_id = {dom_id} AND submissive_id = {sub_id}")
        return self.cursor.fetchone() is not None

    def get_relationship(self, dom_id, sub_id) -> Response:
        self.logger.info(f"Finding relationship between {dom_id} and {sub_id}")
        self.cursor.execute(f"SELECT * FROM Relationships WHERE dominant_id = {dom_id} and submissive_id = {sub_id}")
        data = self.cursor.fetchone()
        return Response(Status.OK, result_to_relationship(data))

    def find_confirmed_relationship(self, dom_id, sub_id) -> Response:
        self.cursor.execute(f'SELECT relationship_id FROM relationships WHERE dominant_id = {dom_id} AND submissive_id = {sub_id} AND pending = 0')
        data = self.cursor.fetchall()
        return Response(Status.OK, result_to_relationship(data))

    def confirm_relationship(self, relationship_id) -> Status:
        self.cursor.execute(f'UPDATE relationships SET pending = 0 WHERE relationship_id = {relationship_id}')
        return Status.OK

    def get_number_of_submissives(self, dom_id) -> int:
        print("Getting number of subs.")
        self.cursor.execute(f'SELECT relationship_id FROM {RELATIONSHIPS} WHERE dominant_id = {dom_id};')
        data = self.cursor.fetchall()
        return len(data)

    def add_relationship(self, relationship: Relationship) -> Status:
        self.cursor.execute(f'INSERT INTO Relationships(dominant_id, submissive_id, initiated_by, pending) VALUES("{relationship.dominant_id}","{relationship.submissive_id}","{relationship.initiated_by}",1);')
        return Status.OK

    def get_all_submissives(self, dom_id: int) -> list:
        self.cursor.execute(f'SELECT submissive_id FROM {RELATIONSHIPS} WHERE dominant_id = {dom_id} AND pending = 0;')
        data = self.cursor.fetchall()
        return Response(Status.OK, result_to_relationship(data))

    #Identities
    def refresh_default_identities(self, guild_id):
        #Delete all identities for given guild belonging to the enforcement drone.
        self.cursor.execute(f'DELETE FROM identities WHERE owner_id = {guild_id} AND owner_type = "guild";')
        #Reinsert the default identities.
        for statement in init_default_identities_for_guild(guild_id):
            self.cursor.execute(statement)

    def get_identity_by_role_name(self, role_name, guild_id) -> Identity:
        self.cursor.execute(f'SELECT * FROM identities WHERE name = "{role_name}" AND owner_id = {guild_id} AND owner_type = "guild";')
        data = self.cursor.fetchall()
        return Response(Status.OK, result_to_identity(data))

    def get_all_identities_for_guild(self, guild_id) -> Identity:
        self.cursor.execute(f'SELECT name, display_name FROM identities WHERE owner_id = {guild_id} AND owner_type = "guild";')
        data = self.cursor.fetchall()
        return Response(Status.OK, result_to_identity(data))

    def get_all_identities_for_user(self, user_id) -> Identity:
        self.cursor.execute(f'SELECT name FROM identities WHERE owner_id = {user_id} AND owner_type = "user";')
        data = self.cursor.fetchall()
        return Response(Status.OK, result_to_identity(data))

    #Users
    def get_registered_user(self, user_id):
        self.cursor.execute(f'SELECT user_id FROM users WHERE user_id = {user_id}')
        data = self.cursor.fetchall()
        return Response(Status.OK, result_to_user(data))
    
    def register_user_with_id(self, user_id, drone_id):
        self.cursor.execute(f'INSERT INTO users(user_id, drone_id) VALUES({user_id}, LPAD({drone_id}, 4, 0));')
        return Status.OK

    def register_user(self, user_id):
        self.cursor.execute(f'INSERT INTO users(user_id) VALUES({user_id});')
        return Status.OK

    def get_all_registered_drones(self):
        self.cursor.execute('SELECT drone_id FROM users')
        data = self.cursor.fetchall()
        return Response(Status.OK, result_to_user(data))