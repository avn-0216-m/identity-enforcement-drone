import discord
from data_classes import Status

class Enforcement_Handler():
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def enforce(self, role: discord.Role = None, member: discord.Member = None):
        print(f"Attempting to enforce {member.display_name} with role {role.name} in {member.guild.name}")
        #Find the identity that corresponds with the role.
        #Roles have the same name as the identity, without the four-pointed star and colon.
        print("Role name to look for: " + role.name)
        identity = self.db.get_identity_by_role(role.name[3:], member.guild.id).data

        

    def refresh_default_identities(self, guild: discord.Guild) -> Status:
        print(f"Refreshing default identities for server {guild.name}")
        self.db.refresh_default_identities(guild.id)
        return Status.OK