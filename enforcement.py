import discord
from discord.utils import get
from data_classes import Status
from webhook import Webhook_Handler
from notable_entities import ENFORCEMENT_PREFIX

class Enforcement_Handler():
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.wh = Webhook_Handler(bot)

    async def enforce(self, message: discord.Message = None, role: discord.Role = None):
        print(f"Attempting to enforce {message.author.display_name} with role {role.name} in {message.author.guild.name}")
        #Find the identity that corresponds with the role.
        #Roles have the same name as the identity, without the four-pointed star and colon.
        print(f"Role name to look for: {role.name}")
        identity = self.db.get_identity_by_role(role.name[3:], message.author.guild.id).data
        if len(identity) == 0:
            print("Someone has a role for an identity that doesn't exist.")
            return
        await self.wh.proxy_message(message = message, identity = identity[0])

    def refresh_default_identities(self, guild: discord.Guild) -> Status:
        print(f"Refreshing default identities for server {guild.name}")
        self.db.refresh_default_identities(guild.id)
        return Status.OK

    async def assign(self, target: discord.Member = None, role: str = None):
        #Check if given string is a valid identity.
        if len(self.db.get_identity_by_role(role, target.guild.id).data) == 0:
            print("Not a valid identity")
            return Status.BAD_REQUEST
        #Check if the server has the enforcable role available.
        role_to_assign = get(target.guild.roles, name=f"{ENFORCEMENT_PREFIX} {role}")
        if role_to_assign is None:
            print("Role not present. Creating.")
            role_to_assign = await target.guild.create_role(name=f"{ENFORCEMENT_PREFIX} {role}")
        #Check if user already has an enforceable role.
        for role in target.roles:
            if role.name.startswith(ENFORCEMENT_PREFIX):
                print("An enforcable role is already present. Removing.")
                await target.remove_roles(role)
        #Finally, assign the new enforcement role.
        await target.add_roles(role_to_assign)
        return Status.OK

    def check_permissions(self, dom_id, sub_id) -> bool:
        if dom_id == sub_id:
            return True

        results = self.db.find_confirmed_relationship(dom_id, sub_id).data
        if len(results) != 0:
            return True
        return False