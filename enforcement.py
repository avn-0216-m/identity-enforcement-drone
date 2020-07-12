import discord
import random
import logging
from discord.utils import get
from data_classes import Status, Enforcement, Identity
from webhook import Webhook_Handler
from notable_entities import ENFORCEMENT_PREFIX
from utils import scrape_drone_id

class Enforcement_Handler():
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.wh = Webhook_Handler(bot)
        self.logger = logging.getLogger("Identity Enforcement Drone")

    async def enforce(self, message: discord.Message = None, role: discord.Role = None):
        self.logger.info(f"Enforcing {message.author.display_name} with role {role.name[3:]} in {message.author.guild.name}")
        #Find the identity that corresponds with the role.
        #Roles have the same name as the identity, without the four-pointed star and colon.
        identity = self.db.get_identity_by_role_name(role.name[3:], message.author.guild.id).data
        if len(identity) == 0:
            self.logger.warning(f"{message.author.display_name} has a role for an identity that doesn't exist ({role.name}). Removing.")
            await message.author.remove_roles(role)
            return
        await self.wh.proxy_message(message = message, identity = identity[0])

    async def get_webhook(self, channel: discord.Channel) -> discord.Webhook:
        self.logger.info(f'Getting a webhook for "{channel.name}"')
        available_webhooks = await channel.webhooks()
        if len(available_webhooks) == 0:
            self.logger.info(f'Creating webhook for "{channel.name}"')
            available_webhooks = [await message.channel.create_webhook(name = "Identity Enforcement Drone")]
        return available_webhooks[0]

    async def enforce_user(self, message: discord.Message, enforcement: Enforcement):
        self.logger.info("In enforce_user function.")
        #Get identity via identity ID from enforcement.
        identity = self.db.get_identity_by_id(enforcement)

        proxy_username = message.author.display_name
        proxy_message_content = ""

        #Drone ID name takes priority over non-drone ID name, so check that first.
        if identity.display_name_with_id is not None and scrape_drone_id(message.author.display_name) is not None:
            #If there is a display name for drones AND the user has an id. Set it.

        elif identity.display_name is not None:
            #If there is a display name to use, set it.
            proxy_username = identity.display_name

        proxy_webhook = get_webhook(message.channel)
        await proxy_webhook.send(proxy_message_content, username=proxy_username)
        return True

    def refresh_default_identities(self, guild: discord.Guild) -> Status:
        self.logger.info(f"Refreshing default identities for guild {guild.name}")
        self.db.refresh_default_identities(guild.id)
        return Status.OK

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

    def check_permissions(self, dom_id, sub_id) -> bool:
        if dom_id == sub_id:
            return True

        results = self.db.find_confirmed_relationship(dom_id, sub_id).data
        if len(results) != 0:
            return True
        return False

    def generate_new_id(self, guild: discord.Guild) -> str:

        preexisting_ids = []

        #Get all registered drone IDs from database.
        drones = self.db.get_all_registered_drones().data

        for drone in drones:
            preexisting_ids.append(drone.drone_id)
        #Get all registered drone IDs from the server.
        for member in guild.members:
            drone_id = scrape_drone_id(member.display_name)
            if drone_id is not None:
                preexisting_ids.append(drone_id)

        generated_id = random.randint(0,9999)
        generated_id = f"{generated_id:04}"

        while generated_id in preexisting_ids:
            generated_id = random.randint(0,9999)
            generated_id = f"{generated_id:04}"

        return generated_id


