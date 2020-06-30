import sqlite3
import discord
from database_constants import DATABASE_NAME, MESSAGES, get_migration, RELATIONSHIPS
from data_classes import Relationship, Identity, Status, Response
from notable_entities import ENFORCEMENT_DRONE
from default_identities import init_default_identities_for_guild
from rowmapper import result_to_identity, result_to_relationship, result_to_user, map_row
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


    #General
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
                                user_id INTEGER,
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
                                user_id INTEGER NOT NULL,
                                guild_id INTEGER NOT NULL
                            );

                            """)
        self.connection.commit()

    #Identities
    def get_all_user_identities(self, user):
        self.cursor.execute("SELECT name, description FROM Identities WHERE user_id = ?", (user.id,))
        data = self.cursor.fetchall()
        return map_row(data, Identity)

    def get_user_identity_by_name(self, user, name: str):
        self.cursor.execute("SELECT * FROM Identities WHERE user_id = ? AND name = ?", (user.id, name))
        data = self.cursor.fetchone()

        self.logger.info(f"DB RESULT IS {data} AND TYPE IS {type(data)}")

        return map_row(data, Identity)
