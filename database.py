import sqlite3
import discord
from data_classes import Relationship, Identity, Status, Response
from notable_entities import ENFORCEMENT_DRONE
from rowmapper import map_rows
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
            #Get a new cursor
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
                                identity_id INTEGER NOT NULL,
                                guild_id INTEGER NOT NULL
                            );

                            """)
        self.connection.commit()

    #Identities
    def get_all_user_identities(self, user):
        self.cursor.execute("SELECT name, description FROM Identities WHERE user_id = ?", (user.id,))
        data = self.cursor.fetchall()
        return map_rows(data, Identity)

    def get_user_identity_by_name(self, user, name: str):
        self.cursor.execute("SELECT * FROM Identities WHERE user_id = ? AND name = ?", (user.id, name))
        data = self.cursor.fetchone()
        return map_rows(data, Identity)

    def create_identity(self, user: discord.Member, name: str):
        self.cursor.execute("INSERT INTO Identities(user_id, name) VALUES(?,?);" (user.id, name))
        self.connection.commit()

    def update_identity(self, identity: Identity, field: str, new_value: str):
        self.cursor.execute("UPDATE Identities SET ? = ? WHERE user_id = ?" (field, new_value, identity.identity_id))
        self.connection.commit()

    #Relationship
    def get_relationship(self, dominant, submissive):
        self.cursor.execute("SELECT * FROM Relationships WHERE dominant_id = ? and submissive_id = ?", (dominant.id, submissive.id))
        data = self.cursor.fetchone()
        return map_rows(data, Identity)

    def add_relationship(self, dominant: discord.Member, submissive: discord.Member, initiated_by: discord.Member):
        try:
            self.cursor.execute("INSERT INTO Relationships(dominant_id, submissive_id, initiated_by) VALUES(?,?,?)", (dominant.id, submissive.id, initiated_by.id))
            self.connection.commit()
            return True
        except:
            self.logger.error("Adding the relationship failed.")
            return False

    def confirm_relationship(self, relationship_id: int):
        try:
            self.cursor.execute("UPDATE Relationships SET pending = 0 WHERE relationship_id = ?", (relationship_id,))
            self.connection.commit()
            return True
        except:
            self.logger.error("Confirming the relationship failed.")
            return False

    def end_relationship(self, relationship: Relationship):
        try:
            self.cursor.execute("DELETE FROM Relationships WHERE relationship_id = ?", (relationship.relationship_id,))
            self.connection.commit()
            return True
        except:
            self.logger.error("Ending the relationship failed.")
            return False

    #Enforcement
    def add_enforcement(self, user, identity, guild):
        self.cursor.execute("INSERT INTO Enforcments(user_id, identity_id, guild_id) VALUES(?,?,?);", (user.id, identity.id, guild.id))
        self.connection.commit()
        return True