from database import Database_Handler
from data_classes import Relationship, Status, Response
import discord

class Relationship_Handler():
    def __init__(self, db):
        self.db = db
        
    def handle_relationship_request(self, dominant: discord.Member, submissive: discord.Member, initiated_by: discord.Member):

        #Validate arguments
        if dominant is not discord.Member or submissive is not discord.Member or initiated_by is not discord.Member: return Status.BAD_REQUEST

        current_relationship = self.db.get_relationship(dominant, submissive)
        if current_relationship is None:
            #No pre-existing relationship, register it in DB.
            self.db.add_relationship(Relationship(dominant = dominant, submissive = submissive, initiated_by = initiated_by))
        elif current_relationship.pending == 1 and current_relationship.initiated_by != initiated_by.id:
            #Relationship mutually confirmed.
            self.db.confirm_relationship(current_relationship.relationship_id)
        else:
            #It's a duplicate request, disregard it.
            return Status.DUPLICATE_REQUEST