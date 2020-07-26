from database import Database
from data_classes import Relationship, Status, Response
import logging
import discord

LOGGER = logging.getLogger("Identity Enforcement Drone")
db = Database()

def handle_relationship_request(dominant: discord.Member, submissive: discord.Member, initiated_by: discord.Member):

    if (current_relationship := db.get_relationship(dominant, submissive)) is None:
        LOGGER.info(f"No prexisting relationship between {dominant.name} and {submissive.name}")
        #No pre-existing relationship, register it in DB.
        db.add_relationship(dominant = dominant, submissive = submissive, initiated_by = initiated_by)
        return Status.CREATED
    elif current_relationship.confirmed == 0 and current_relationship.initiated_by != initiated_by.id:
        LOGGER.info(f"Relationship mutually confirmed between {dominant.name} and {submissive.name}. Relationship ID: {current_relationship.relationship_id}")
        db.confirm_relationship(current_relationship)
        return Status.HOLY_MATRIHORNY
    else:
        LOGGER.info(f"Discarding duplicate relationship request from {initiated_by}")
        #It's a duplicate request, disregard it.
        return Status.DUPLICATE_REQUEST