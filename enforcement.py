import discord
import re
import random
import logging
from discord.utils import get
from database import Database
from data_classes import Status, Enforcement, Identity
from notable_entities import ENFORCEMENT_PREFIX
from serialize import string_to_lexicon

db = Database()

LOGGER = logging.getLogger("Identity Enforcement Drone")

async def get_webhook(channel: discord.channel) -> discord.Webhook:
    available_webhooks = await channel.webhooks()
    if len(available_webhooks) == 0:
        available_webhooks = [await channel.create_webhook(name = "Identity Enforcement Drone")]
    return available_webhooks[0]

def get_drone_id(display_name: str) -> str:
    try:
        return re.search(r"\d{4}", display_name).group()
    except AttributeError:
        return None

async def enforce_user(message: discord.Message, enforcement: Enforcement):
    LOGGER.info("In enforce_user function.")
    #Get identity via identity ID from enforcement.
    identity = db.get_identity_by_id(enforcement.identity_id)

    proxy_username = message.author.display_name
    proxy_avatar_url = message.author.avatar_url
    proxy_message_content = message.content

    #Enforce the display name (drone ID) if applicable.

    LOGGER.debug(get_drone_id(message.author.display_name))

    if identity.display_name_with_id is not None and (drone_id := get_drone_id(message.author.display_name)) is not None:
        LOGGER.debug("Setting proxy name to use drone ID.")
        proxy_username = identity.display_name_with_id.format(drone_id)

    #Enforce the display name if applicable.
    elif identity.display_name is not None:
        #If there is a display name to use, set it.
        proxy_username = identity.display_name

    #Enforce the avatar if applicable.
    if identity.avatar is not None:
        proxy_avatar_url = identity.avatar

    #Enforce the message body if applicable.
    if identity.replacement_lexicon is not None and identity.allowance_lexicon is None:
        #ENFORCEMENT MODE 1: Replace message with words from the replacement lexicon to a similar length.
        LOGGER.debug(f"ENFORCEMENT MODE 1. Replacement lexicon: {identity.replacement_lexicon}")
        replacement_lexicon = string_to_lexicon(identity.replacement_lexicon)
        proxy_message_content = f"{random.choice(replacement_lexicon)} "
        for word in range(1, len(message.content)//5):
            proxy_message_content += f"{random.choice(replacement_lexicon)} "

    elif identity.replacement_lexicon is not None and identity.allowance_lexicon is not None:
        LOGGER.debug(f"ENFORCEMENT MODE 2. Replacement lexicon: {identity.replacement_lexicon} and Allowance lexicon: {identity.allowance_lexicon}")
        #ENFORCEMENT MODE 2: Replace message with words from the replacement lexicon, and insert any allowed words from the original message roughly where they first occured.
        pass

    elif identity.replacement_lexicon is None and identity.allowance_lexicon is not None:
        LOGGER.debug(f"ENFORCEMENT MODE 3. Allowance lexicon: {identity.allowance_lexicon}")
        #ENFORCEMENT MODE 3: If the message content does not equal a sentence in the allowance lexicon, delete it.
        allowance_lexicon = string_to_lexicon(identity.allowance_lexicon)
        if message.content not in allowance_lexicon:
            await message.delete()

    #The message only needs to be proxied if any of the 3 fields have changed via enforcement (message, avatar, or username).
    if (proxy_message_content == message.content) and (proxy_avatar_url == message.author.avatar_url) and (proxy_username == message.author.display_name):
        return

    proxy_webhook = await get_webhook(message.channel)
    await message.delete()
    await proxy_webhook.send(proxy_message_content, username=proxy_username, avatar_url = proxy_avatar_url)

    return True