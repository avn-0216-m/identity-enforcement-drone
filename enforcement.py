import discord
import random
import logging
from discord.utils import get
from data_classes import Status, Enforcement, Identity
from webhook import Webhook_Handler
from notable_entities import ENFORCEMENT_PREFIX
from utils import scrape_drone_id

async def get_webhook(channel: discord.channel) -> discord.Webhook:
    available_webhooks = await channel.webhooks()
    if len(available_webhooks) == 0:
        available_webhooks = [await message.channel.create_webhook(name = "Identity Enforcement Drone")]
    return available_webhooks[0]

class Enforcement_Handler():
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.wh = Webhook_Handler(bot)
        self.logger = logging.getLogger("Identity Enforcement Drone")

    async def enforce_user(self, message: discord.Message, enforcement: Enforcement):
        self.logger.info("In enforce_user function.")
        #Get identity via identity ID from enforcement.
        identity = self.db.get_identity_by_id(enforcement)

        proxy_username = message.author.display_name
        proxy_message_content = "DEFAULT"

        #Drone ID name takes priority over non-drone ID name, so check that first.
        if identity.display_name_with_id is not None and scrape_drone_id(message.author.display_name) is not None:
            #If there is a display name for drones AND the user has an id. Set it.
            pass

        elif identity.display_name is not None:
            #If there is a display name to use, set it.
            proxy_username = identity.display_name

        #TODO: The rest of the enforcement workflow (message content etc)

        proxy_webhook = await get_webhook(message.channel)
        await message.delete()
        await proxy_webhook.send(proxy_message_content, username=proxy_username)

        return True

    async def assign(self, target: discord.Member = None, role: str = None):
        #Check if given string is a valid identity.
        if len(self.db.get_identity_by_role_name(role, target.guild.id).data) == 0:
            return Status.BAD_REQUEST
        #Check if the server has the enforcable role available.
        role_to_assign = get(target.guild.roles, name=f"{ENFORCEMENT_PREFIX} {role}")
        if role_to_assign is None:
            self.logger.info(f'Creating enforcable role "{role}" in {target.guild.name}.')
            role_to_assign = await target.guild.create_role(name=f"{ENFORCEMENT_PREFIX} {role}")
        #Check if user already has an enforceable role.
        for role in target.roles:
            if role.name.startswith(ENFORCEMENT_PREFIX):
                print("An enforcable role is already present. Removing.")
                await target.remove_roles(role)
        #Finally, assign the new enforcement role.
        await target.add_roles(role_to_assign)
        return Status.OK