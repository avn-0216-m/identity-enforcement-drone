import discord
from data_classes import Identity
from serialize import string_to_lexicon
from utils import scrape_drone_id
import logging
import random
import re

class Webhook_Handler():
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('Identity Enforcement Drone')

    def get_occurrences_of_allowance_lexicon(self, allowance_lexicon: str, message: str) -> list:
        allowance_lexicon = string_to_lexicon(allowance_lexicon)
        occurrences = []
        for word in allowance_lexicon:
            occurrences.extend((m.start(), word) for m in re.finditer(word, message))
        occurrences.sort(key=lambda x: x[0])
        return occurrences

    async def get_webhook_for(self, message: discord.Message = None) -> discord.Webhook:
        self.logger.info(f'Getting a webhook for "{message.channel.name}" in "{message.guild.name}".')
        available_webhooks = await message.channel.webhooks()
        if len(available_webhooks) == 0:
            self.logger.info(f'Creating webhook for channel "{message.channel.name}" in "{message.guild.name}"')
            available_webhooks = [await message.channel.create_webhook(name = "Identity Enforcement Drone")]
        return available_webhooks[0]

    async def proxy_message(self, message: discord.Message = None, identity: Identity = None):
        webhook = await self.get_webhook_for(message)

        message_content = message.content

        proxy_name = identity.display_name if identity.display_name is not None else message.author.display_name

        drone_id = scrape_drone_id(message.author.display_name)
        #(If drone ID is none here, check DB to see if user has a drone ID there)

        if drone_id is not None and identity.display_name_with_id is not None:
            print("User has a drone ID. Enforcing drone ID display name.")
            proxy_name = identity.display_name_with_id.format(drone_id)

        
        self.logger.info(f"Identity's strictness value is: {identity.strict}")
            

        if identity.replacement_lexicon != None and identity.allowance_lexicon != None:
            self.logger.info(f'Enforcing "{message.author}" with allowed words and the replacement lexicon.')
            #Use lexicon, insert allowed words when they occur.
            occurrences = self.get_occurrences_of_allowance_lexicon(identity.allowance_lexicon, message.content)
            print("Lexicon and allowed words detected.")
            lexicon = string_to_lexicon(identity.replacement_lexicon)
            allowance_lexicon = string_to_lexicon(identity.allowance_lexicon)
            print("Lexicon and allowed words parsed. Replacing message.")
            message_content = ""
            for i in range(0,len(message.content)//5 + 1):
                message_content += f"{random.choice(lexicon)} "
                if occurrences is not None and len(occurrences) != 0 and len(message_content) > occurrences[0][0]:
                    message_content += str(occurrences.pop(0)[1]) + " "

        elif identity.replacement_lexicon != None and identity.allowance_lexicon == None:
            self.logger.info(f'Enforcing "{message.author}" with their identity\'s replacement lexicon.')
            lexicon = string_to_lexicon(identity.replacement_lexicon)
            message_content = random.choice(lexicon)
            for i in range(0,len(message.content)//5 + 1):
                message_content += f"{random.choice(lexicon)} "

        elif identity.replacement_lexicon == None and identity.allowance_lexicon != None and identity.strict == 1:
            self.logger.info(f'Enforcing "{message.author}" with strict speech restrictions.')
            print("Allowed words detected without lexicon. Strict speech restriction enabled.")

            if drone_id is not None:
                allowance_lexicon = [word.format(drone_id) for word in string_to_lexicon(identity.allowance_lexicon)]
            else:
                allowance_lexicon = string_to_lexicon(identity.allowance_lexicon)

            if message.content not in allowance_lexicon:
                await message.delete()
                return

        elif identity.replacement_lexicon == None and identity.allowance_lexicon != None and identity.strict == 0:
            self.logger.warning("Relaxed allowance lexicons are not implemented.")

            #If this point is reached, the allowance lexicon will need to be checked (and altered if necessary) to only contain single words.
            #Unless I can think of a smarter way to do things.
            #Which is unlikely, as I am a dumbass.

            return

        await message.delete()
        await webhook.send(message_content, username=proxy_name, avatar_url = identity.avatar)


