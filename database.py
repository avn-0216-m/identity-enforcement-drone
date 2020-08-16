import sqlite3
import discord
from data_classes import Relationship, Identity, Status, Response, Enforcement
from notable_entities import ENFORCEMENT_DRONE
from rowmapper import map_rows
from default_identities import DEFAULT_IDENTITIES
import logging
import sys

class Database():

    database_name = "identity_enforcement_drone.sqlite3"
    connection = None
    cursor = None

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self):

        self.logger = logging.getLogger("Identity Enforcement Drone")

        if Database.connection is None:
            #Create a new connection.
            new_connection = sqlite3.connect(Database.database_name)
            new_connection.row_factory = self.dict_factory
            Database.connection = new_connection
        self.connection = Database.connection
        if Database.cursor is None:
            #Get a new cursor
            Database.cursor = Database.connection.cursor()
        self.cursor = Database.cursor


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
                                confirmed INTEGER DEFAULT 0
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

    def delete_user_identity_by_name(self, user, name: str):
        try:
            self.cursor.execute("DELETE FROM Identities WHERE user_id = ? AND name = ?", (user.id, name))
            self.connection.commit()
            return True
        except:
            self.logger.error("Something went wrong with deleting user identity.")
            return False

    def get_identity_by_id(self, identity_id: int):
        self.cursor.execute("SELECT * FROM Identities WHERE identity_id = ?", (identity_id,))
        return map_rows(self.cursor.fetchone(), Identity)

    def create_identity(self, user: discord.Member, identity_name: str):
        '''
        Creates a barebones identity with only a name and an owner ID in the database.
        '''
        self.cursor.execute("INSERT INTO Identities(user_id, name) VALUES(?,?);", (user.id, identity_name))
        self.connection.commit()

    def create_identity(self, identity: Identity):
        '''
        Creates an identity entry in the DB
        with whatever values are present in the provided identity object.
        '''
        self.cursor.execute("""
        INSERT INTO Identities(
            name,
            description,
            display_name,
            display_name_with_id,
            avatar,
            replacement_lexicon,
            allowance_lexicon,
            strict,
            override_lexicon,
            override_chance,
            user_id)
        VALUES(?,?,?,?,?,?,?,?,?,?,?);
        """, (identity.name, identity.description, identity.display_name, identity.display_name_with_id, identity.avatar, identity.replacement_lexicon, identity.allowance_lexicon, identity.strict, identity.override_lexicon, identity.override_chance, identity.user_id))
        self.connection.commit()
        return True

    def update_identity(self, identity: Identity, field: str, new_value: str):
        self.cursor.execute(f"UPDATE Identities SET {field} = ? WHERE identity_id = ?", (new_value, identity.identity_id))
        self.connection.commit()

    def set_default_identities(self, user: discord.Member):
        for identity in DEFAULT_IDENTITIES:
            self.cursor.execute("DELETE FROM Identities WHERE user_id = ? AND name = ?;", (user.id, identity.name))
            self.cursor.execute("""
                                INSERT INTO Identities(
                                    name,
                                    description,
                                    display_name,
                                    display_name_with_id,
                                    avatar,
                                    replacement_lexicon,
                                    allowance_lexicon,
                                    strict,
                                    override_lexicon,
                                    override_chance,
                                    user_id)
                                VALUES(?,?,?,?,?,?,?,?,?,?,?);
                                """, (identity.name, identity.description, identity.display_name, identity.display_name_with_id, identity.avatar, identity.replacement_lexicon, identity.allowance_lexicon, identity.strict, identity.override_lexicon, identity.override_chance, user.id))
        self.connection.commit()
        return True

    #Relationship
    def get_relationship(self, dominant, submissive):
        self.cursor.execute("SELECT * FROM Relationships WHERE dominant_id = ? AND submissive_id = ?", (dominant.id, submissive.id))
        data = self.cursor.fetchone()
        return map_rows(data, Relationship)

    def get_all_pending_relationships(self, user):
        self.cursor.execute("SELECT * FROM Relationships WHERE (submissive_id = ? OR dominant_id = ?) AND confirmed = 0", (user.id, user.id))
        return map_rows(self.cursor.fetchall(), Relationship)

    def delete_all_pending_relationships(self, user):
        self.cursor.execute("DELETE FROM Relationships WHERE (submissive_id = ? OR dominant_id = ?) AND confirmed = 0", (user.id, user.id))
        self.connection.commit()

    def get_all_relationships_where_user_is_sub(self, user):
        self.cursor.execute("SELECT * FROM Relationships WHERE submissive_id = ? AND confirmed = 1", (user.id,))
        return map_rows(self.cursor.fetchall(), Relationship)

    def get_all_relationships_where_user_is_dom(self, user):
        self.cursor.execute("SELECT * FROM Relationships WHERE dominant_id = ? AND confirmed = 1", (user.id,))
        return map_rows(self.cursor.fetchall(), Relationship)

    def add_relationship(self, dominant: discord.Member, submissive: discord.Member, initiated_by: discord.Member):
        try:
            self.cursor.execute("INSERT INTO Relationships(dominant_id, submissive_id, initiated_by) VALUES(?,?,?)", (dominant.id, submissive.id, initiated_by.id))
            self.connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"Adding the relationship failed: {e}")
            return False

    def confirm_relationship(self, relationship: Relationship):
        try:
            self.logger.info(f"Confirming relationship ID: {relationship.relationship_id}")
            self.cursor.execute("UPDATE Relationships SET confirmed = 1 WHERE relationship_id = ?", (relationship.relationship_id,))
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
        self.cursor.execute("INSERT INTO Enforcements(user_id, identity_id, guild_id) VALUES(?,?,?);", (user.id, identity.identity_id, guild.id))
        self.connection.commit()
        return True

    def end_enforcement_by_user_and_guild(self, user, guild):
        self.cursor.execute("DELETE FROM Enforcements WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
        self.connection.commit()

    def get_all_guild_enforcements(self, guild):
        self.cursor.execute("SELECT user_id, identity_id FROM Enforcements WHERE guild_id = ?", (guild.id,))
        return map_rows(self.cursor.fetchall(), Enforcement)

    def end_enforcement_by_enforcement(self, enforcement):
        try:
            self.cursor.execute("DELETE FROM Enforcements WHERE enforcement_id = ?", (enforcement.enforcement_id,))
            self.connection.commit()
            return True
        except:
            self.logger.error("Something went wrong with ending the enforcement via enforcement ID.")
            return False

    def get_enforcement(self, user, guild):
        self.cursor.execute("SELECT enforcement_id, identity_id FROM Enforcements WHERE user_id = ? AND guild_id = ?", (user.id, guild.id))
        return map_rows(self.cursor.fetchone(), Enforcement)

    def end_all_enforcements_of_identity(self, identity):
        try:
            self.logger.info(f"Deleting all enforcements of identity ID {identity.identity_id}")
            self.cursor.execute("DELETE FROM Enforcements WHERE identity_id = ?", (identity.identity_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"Deleting all enforcements of identity {identity.identity_id} failed: {e}")
            return False

    def update_enforcement(self, enforcement, new_identity):
        self.logger.debug(f"Updating enforcement. Enforcement ID: {enforcement.enforcement_id}, Identity ID: {new_identity.identity_id}")
        self.cursor.execute("UPDATE Enforcements SET identity_id = ? WHERE enforcement_id = ?", (new_identity.identity_id, enforcement.enforcement_id))
        self.connection.commit()
        return True