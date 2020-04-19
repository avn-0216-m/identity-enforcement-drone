import discord
from data_classes import Status

class Enforcement_Handler():
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def enforce(self, role: discord.Role = None, member: discord.Member = None):
        print(f"Attempting to enforce {member.display_name} with role {role.name} in {member.guild.name}")
        #Find the identity that corresponds with the role.

    def refresh_default_identities(self, guild: discord.Guild) -> Status:
        print(f"Refreshing default identities for server {guild.name}")
        self.db.refresh_default_identities(guild.id)
        return Status.OK