from database import Database_Handler
from data_classes import Relationship, Status, Response
import logging
import discord

class Relationship_Handler():
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger("Identity Enforcement Drone")
        
    def handle_relationship_request(self, dominant: discord.Member, submissive: discord.Member, initiated_by: discord.Member):

        if (current_relationship := self.db.get_relationship(dominant, submissive)) is None:
            self.logger.info(f"No prexisting relationship between {dominant.name} and {submissive.name}")
            #No pre-existing relationship, register it in DB.
            self.db.add_relationship(dominant = dominant, submissive = submissive, initiated_by = initiated_by)
            return Status.CREATED
        elif current_relationship.confirmed == 0 and current_relationship.initiated_by != initiated_by.id:
            self.logger.info(f"Relationship mutually confirmed between {dominant.name} and {submissive.name}. Relationship ID: {current_relationship.relationship_id}")
            self.db.confirm_relationship(current_relationship)
            return Status.HOLY_MATRIHORNY
        else:
            self.logger.info(f"Discarding duplicate relationship request from {initiated_by}")
            #It's a duplicate request, disregard it.
            return Status.DUPLICATE_REQUEST