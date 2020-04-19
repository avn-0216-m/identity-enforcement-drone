import discord

class Enforcement_Handler():
    def __init__(self, bot):
        self.bot = bot

    def enforce(self, role: discord.Role = None, member: discord.Member = None):
        print(f"Attempting to enforce {member.display_name} with role {role.name}")
        #Find the identity that corresponds with the role.

    def refresh_default_identities(self, guild: discord.Guild) -> Status:
        print(f"Refreshing default identities for server {guild.name}")
        
        return Status.OK