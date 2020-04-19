import discord
from data_classes import Status
from webhook import Webhook_Handler

class Enforcement_Handler():
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.wh = Webhook_Handler(bot)

    async def enforce(self, message: discord.Message = None, role: discord.Role = None):
        print(f"Attempting to enforce {message.author.display_name} with role {role.name} in {message.author.guild.name}")
        #Find the identity that corresponds with the role.
        #Roles have the same name as the identity, without the four-pointed star and colon.
        print("Role name to look for: " + role.name)
        identity = self.db.get_identity_by_role(role.name[3:], message.author.guild.id).data
        await self.wh.proxy_message(message = message, identity = identity)

    def refresh_default_identities(self, guild: discord.Guild) -> Status:
        print(f"Refreshing default identities for server {guild.name}")
        self.db.refresh_default_identities(guild.id)
        return Status.OK