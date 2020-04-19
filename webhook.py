import discord
from data_classes import Identity
from serialize import string_to_lexicon
import random
import re

class Webhook_Handler():
    def __init__(self, bot):
        self.bot = bot

    def get_occurrences_of_allowed_words(self, allowed_words: str, message: str) -> list:
        allowance_lexicon = string_to_lexicon(allowed_words)
        occurrences = []
        for word in allowance_lexicon:
            occurrences.extend((m.start(), word) for m in re.finditer(word, message))
        occurrences.sort(key=lambda x: x[0])
        return occurrences

    async def get_webhook_for(self, message: discord.Message = None) -> discord.Webhook:
        print("Getting a webhook.")
        available_webhooks = await message.channel.webhooks()
        if len(available_webhooks) == 0:
            print(f"No webhook found. Creating webhook for channel {message.channel.name}")
            available_webhooks = [await message.channel.create_webhook(name = "Identity Enforcement Drone")]
        return available_webhooks[0]

    async def proxy_message(self, message: discord.Message = None, identity: Identity = None):
        print("Proxying message.")
        webhook = await self.get_webhook_for(message)
        message_content = message.content

        occurrences = None

        if identity.allowed_words != "":
            print("Allowed words detected. Gathering occurrences.")
            occurrences = self.get_occurrences_of_allowed_words(identity.allowed_words, message.content)

        if identity.lexicon is not None:
            print("Lexicon detected.")
            lexicon = string_to_lexicon(identity.lexicon)
            allowed_words = string_to_lexicon(identity.allowed_words)
            print("Lexicon parsed. Replacing message.")
            message_content = ""
            for i in range(0,len(message.content)//5 + 1):
                message_content += f"{random.choice(lexicon)} "
                if occurrences is not None and len(occurrences) != 0 and len(message_content) > occurrences[0][0]:
                    message_content += str(occurrences.pop(0)[1]) + " "

        await message.delete()
        await webhook.send(message_content, username=identity.display_name, avatar_url = identity.avatar)

