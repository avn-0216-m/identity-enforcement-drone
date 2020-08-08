#!/usr/bin/python

#import core modules
import sys
import discord
import logging
from discord.ext import commands
import json
import asyncio
import random
import traceback

#import handler modules
import relationship as rl
import enforcement as en
from database import Database
#import utility modules 
from notable_entities import ENFORCEMENT_PREFIX, ENFORCEMENT_DRONE, SERIALIZER_DIVIDER
from serialize import lexicon_to_string
import text
from enforcement import get_webhook
#import data structure modules
from data_classes import Status, Identity
from default_identities import DEFAULT_IDENTITIES

#Setup logger
logger = logging.getLogger('Identity Enforcement Drone')
formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d :: %(levelname)s :: %(message)s', datefmt='%Y-%m-%d :: %H:%M:%S')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
fh = logging.FileHandler('log.txt')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

logger.info("-----------------------------------------------")
logger.info("It's a new day~!")
logger.info("-----------------------------------------------")

# Valid attributes for certain commands
viewable_attributes = ["display_name", "name", "description", "replacement_lexicon", "allowance_lexicon", "user_id"]
addable_attributes = ["replacement_lexicon", "allowance_lexicon", "override_lexicon"]
settable_attributes = ["name", "description", "replacement_lexicon", "avatar", "display_name"]
# TODO: add all necessary attributes

bot = commands.Bot(command_prefix="!", case_insensitive=True)

logger.info("Loading secret details from file.")
with open("bot_token.txt") as secret_file:
    bot_token = secret_file.readline()

#Initalize DAO
db = Database()

#Commands
@bot.group(invoke_without_command = True, aliases=["rel", "rl", "relationship"])
async def relationships(context):

    dom_list_text = ""
    sub_list_text = ""
    external_doms = 0
    external_subs = 0

    dom_list = db.get_all_relationships_where_user_is_sub(context.author)
    sub_list = db.get_all_relationships_where_user_is_dom(context.author)

    if dom_list is not None and len(dom_list) > 0:
        for relationship in dom_list:
            dom_user = context.guild.get_member(relationship.dominant_id)
            if dom_user is not None:
                dom_list_text += dom_user.display_name + "\n"
            else:
                external_doms += 1
    else:
        dom_list_text = "You have no dominants"

    if sub_list is not None and len(sub_list) > 0:
        for relationship in sub_list:
            sub_user = context.guild.get_member(relationship.submissive_id)
            if sub_user is not None:
                sub_list_text += sub_user.display_name + "\n"
            else:
                external_subs += 1
    else:
        sub_list_text = "You have no submissives."

    if external_subs > 0:
        sub_list_text += f"...and {external_subs} more on other server(s)!"
    if external_doms > 0:
        dom_list_text += f"...and {external_doms} more on other server(s)!"

    reply = discord.Embed(title="Your relationships:")
    reply.add_field(name="Submissives:", value=sub_list_text, inline=False)
    reply.add_field(name="Dominants:",value=dom_list_text, inline=False)
    await context.send(embed=reply)

@relationships.group(invoke_without_command = True)
async def pending(context):

    reply = discord.Embed(title="Incoming relationship requests in this server:")

    pending_doms = ""
    pending_subs = ""

    pending_relationships = db.get_all_pending_relationships(context.author)

    if pending_relationships is None or len(pending_relationships) == 0:
        reply.description = "You have no pending submissives or dominants."
        await context.send(embed=reply)
        return

    for relationship in pending_relationships:
        if relationship.submissive_id == context.author.id:
            pending_user = context.guild.get_member(relationship.dominant_id)
            if pending_user is None:
                continue
            else:
                pending_doms += f"{pending_user.display_name}\n"
        else:
            pending_user = context.guild.get_member(relationship.submissive_id)
            if pending_user is None:
                continue
            else:
                pending_subs += f"{pending_user.display_name}\n"

    else:
        if pending_doms != "":
            reply.add_field(name = "Pending dominants:", value = pending_doms, inline = False)
        if pending_subs != "":
            reply.add_field(name = "Pending submissives:", value = pending_subs, inline = False)

    await context.send(embed=reply)

@pending.command()
async def clear(context):
    db.delete_all_pending_relationships(context.author)
    await context.send(embed=discord.Embed(title="All incoming pending relationships have been cleared."))

@relationships.command(aliases = ['dom'])
async def dominate(context, submissive: discord.Member):
    '''
    Attempt to dominate someone
    They must respond by submitting to you with the submit command.
    '''

    if type(submissive) is not discord.Member: 
        return #Bad request!!

    logger.info(f'{context.message.author.display_name} is trying to dominate {submissive.display_name}')

    if context.message.author is submissive:
        await context.send("You cannot own yourself.")
        return

    if submissive.id == ENFORCEMENT_DRONE:
        await context.send("Thanks, but no thanks.")
        return

    response = rl.handle_relationship_request(context.message.author, submissive, context.message.author)
    if response is Status.DUPLICATE_REQUEST:
        await context.send("You are already dominating/attempting to dominate that person.")
    elif response is Status.CREATED:
        await context.send("Request to dominate recieved. The sub will need to submit to you with the 'submit' command.")
    elif response is Status.HOLY_MATRIHORNY:
        reply = discord.Embed(title = "Relationship confirmed! 🎉", description = f"{context.message.author.display_name} is now dominating {submissive.display_name}")
        reply.set_footer(text = random.choice(text.new_relationship))
        await context.send(embed=reply)

@relationships.command(aliases = ['sub'])
async def submit(context, dominant: discord.Member):
    '''
    Attempt to submit to someone
    They must respond by dominating you with the dominate command.
    '''

    if type(dominant) is not discord.Member: return

    logger.info(f'{context.message.author.display_name} is trying to submit to {dominant.display_name}')

    if context.message.author is dominant:
        await context.send("You cannot submit to yourself.")
        return

    if dominant.id == ENFORCEMENT_DRONE:
        await context.send("Thanks, but no thanks.")
        return

    response = rl.handle_relationship_request(dominant, context.message.author, context.message.author)
    if response is Status.DUPLICATE_REQUEST:
        await context.send("You are already submissive to/attempting to submit to that person. You needy fucking bottom, chill out.")
    elif response is Status.CREATED:
        await context.send("Get ready to keysmash in delight- your request to submit has been received. Now the other party simply needs to dominate you in turn.")
    elif response is Status.HOLY_MATRIHORNY:
        reply = discord.Embed(title = "Relationship confirmed! 🎉", description = f"{context.message.author.display_name} is now submissive to {dominant.display_name}")
        reply.set_footer(text = random.choice(text.new_relationship))
        await context.send(embed=reply)

@relationships.command(aliases = ['yeet', 'uncollar', 'goodbye'])
async def relinquish(context, target: discord.Member = None):
    #Validate argument
    if type(target) is not discord.Member:
        return

    reply = discord.Embed(title = f"Relationship changes: {context.message.author.display_name}")
    reply_info = ""

    #End relationship where user is submissive to target
    sub_relationship = db.get_relationship(target, context.message.author)
    if sub_relationship is not None and sub_relationship.confirmed == 1:
        db.end_relationship(sub_relationship)
        reply.add_field(inline = False, name = "No longer submissive to:", value = target.display_name)

    #End relationship where user is dominant to target
    dom_relationship = db.get_relationship(context.message.author, target)
    if dom_relationship is not None and dom_relationship.confirmed == 1:
        db.end_relationship(dom_relationship)
        reply.add_field(inline = False, name = "No longer dominant to:", value = target.display_name)

    reply.set_footer(text = random.choice(text.end_relationship))
    await context.send(embed = reply)
    
@bot.command(aliases = ['init', 'gimmie'])
async def defaults(context):
    db.set_default_identities(context.message.author)
    reply = discord.Embed(title = f"Identities added for {context.message.author.display_name}:")
    for identity in DEFAULT_IDENTITIES:
        reply.add_field(inline = False, name = identity.name, value = identity.description)
    await context.send(embed = reply)

@bot.group(invoke_without_command = True, aliases = ["id", "ids", "identity"])
async def identities(context):
    '''
    This command lists identities for you if invoked without any mentions,
    or lists the identities of anyone mentioned (@user).
    '''

    if len(context.message.mentions) == 0:
        reply = "Your identities are:\n"
        identities = db.get_all_user_identities(context.author)
        for identity in identities:
            reply += f"{identity.name} - {identity.description}\n"

        await context.send(reply)

    else:
        for mention in context.message.mentions:
            reply = f"IDs belonging to {mention}:\n"
            identities = db.get_all_user_identities(mention)

            if len(identities) == 0:
                reply += "None!"
            else:
                for identity in identities:
                    reply += f"{identity.name} - {identity.description}\n"
            await context.send(reply)

@identities.command()
async def new(context, id_name = None, id_desc = None, *id_words):

    if db.get_user_identity_by_name(context.author, id_name) is not None:
        await context.send("Sorry, that identity already exists in your inventory.")
        return

    if id_name is None:
        await context.send("No name provided.")
        return

    lexicon_string = lexicon_to_string(id_words)

    new_identity = Identity(name = id_name, user_id = context.author.id, description = id_desc, replacement_lexicon = lexicon_string)

    db.create_identity(new_identity)

    reply = discord.Embed(title="New identity created. 🎉")
    reply.add_field(name="Name:", value=id_name, inline=False)
    reply.add_field(name="Description:", value=id_desc, inline=False)
    reply.add_field(name="Replacement words:", value=id_words, inline=False)

    await context.send(embed=reply)

@identities.command()
async def add(context, id_name, attribute, words):
    await context.send(f"Adding {words} to {attribute} for {id_name}")

@identities.command()
async def remove(context, id_name, attribute, words):
    await context.send(f"Removing {words} from {attribute} for {id_name}")

@identities.command()
async def delete(context, id_name, please = None):

    if please is None:
        await context.send("Please add 'please' to the end of this command to confirm that you understand this will delete your identity (hot).")
        return

    identity = db.get_user_identity_by_name(context.author, id_name)

    if identity is None:
        await context.send("Good news! That identity already doesn't exist. Huzzah!")
        return

    db.delete_user_identity_by_name(context.author, id_name)

    await context.send(f"Deleting identity {id_name}")

@identities.command(name = "set")
async def _set(context, id_name, attribute, *new_values):
    
    if attribute is None or attribute not in settable_attributes:
        reply = discord.Embed(title="No valid attribute found.", description="Settable attributes are:\nname\ndescription\ndisplay_name\nreplacement_lexicon\navatar_url")
        await context.send(embed=reply)
        return

    identity = db.get_user_identity_by_name(context.author, id_name)

    if identity is None:
        await context.send(embed=discord.Embed(title="No identity by that name found.", description=f"You can list identities you own with '{bot.command_prefix}identities'"))
        return

    if "lexicon" in attribute:
        update_value = lexicon_to_string(new_values)
    else:
        update_value = new_values[0]

    db.update_identity(identity, attribute, update_value)

    reply = discord.Embed(title=f"{id_name} successfully updated.")
    reply.add_field(name=f"New {attribute}:",value=new_values if len(new_values) > 1 else new_values[0])

    if attribute == "avatar":
        reply.set_thumbnail(url=new_values[0])

    await context.send(embed=reply)

@identities.command()
async def view(context, id_name, attribute = None):

    if attribute is None or attribute not in viewable_attributes:
        reply = discord.Embed(title="No valid attribute found.", description="Viewable attributes are:\nname\ndescription\ndisplay_name\nreplacement_lexicon\nallowance_lexicon\noverride_lexicon\noverride_chance\nuser_id")
        await context.send(embed=reply)
        return
    
    identity = db.get_user_identity_by_name(context.author, id_name)

    if identity is None:
        await context.send(embed=discord.Embed(title="No identity by that name found.", description=f"You can list identities you own with '{bot.command_prefix}identities'"))
        return

    reply = discord.Embed(title=f"{id_name}:")
    reply.add_field(name=attribute, value=getattr(identity, attribute).replace(SERIALIZER_DIVIDER, "\n"))

    await context.send(embed = reply)

@identities.command(aliases = ['assign'])
async def enforce(context, target: discord.Member, identity_name: str, global_indicator: str = None):
    '''
    Assign an identity to a user.
    '''

    logger.info(f"Enforcement command triggered. {context.message.author.name} wants to enforce {target.name} with the identity {identity_name} in {context.guild.name}")

    #Confirm the user has the specified identity
    if (identity := db.get_user_identity_by_name(context.message.author, identity_name)) is None:
        await context.send("You do not have that specified identity.")

    #Confirm the user is domming the target
    if target.id != context.author.id:
        if (relationship := db.get_relationship(context.message.author, target)) is None or relationship.confirmed != 1:
            reply = discord.Embed(title = f"Could not enforce {target.display_name}", description = "You must be dominating that user to enforce them with an identity.")
            reply.set_footer(text = random.choice(text.not_domming).format(identity.name))

            await context.send(embed=reply)
            return

    #If the user is already enforced, update the identity
    if (current_enforcement := db.get_enforcement(target, context.guild)) is not None:
        logger.info(f"Updating enforcement for {target.id} with new identity {identity.identity_id}")
        db.update_enforcement(current_enforcement, identity)

        former_identity = db.get_identity_by_id(current_enforcement.identity_id)
        reply = discord.Embed(title = f"Enforcement for {target.display_name} has been updated.")
        reply.add_field(name = "Former identity:", value = former_identity.name)
        reply.add_field(name = "New identity:", value = identity.name)
        reply.set_footer(text = random.choice(text.new_enforcement).format(identity.name))

        await context.send(embed=reply)
        return

    #Otherwise, add an enforcement record in the enforcement table.
    logger.info(f"Adding new enforcement for {target.id} with new identity {identity.identity_id}")
    db.add_enforcement(target, identity, context.guild)

    reply = discord.Embed(title = f"Enforcement for {target.display_name} has been updated.")
    reply.add_field(name = "Former identity:", value = "Themselves")
    reply.add_field(name = "New identity:", value = identity.name)
    reply.set_footer(text = random.choice(text.new_enforcement).format(identity.name))
    await context.send(embed = reply)

@identities.command()
async def release(context, target: discord.Member):
    logger.info(f"Release command triggered. {context.message.author.name} wants to release {target.name} in {context.guild.name}")

    current_enforcement = db.get_enforcement(target, context.guild)
    former_identity = db.get_identity_by_id(current_enforcement.identity_id)

    db.end_enforcement(target, context.guild)

    reply = discord.Embed(title = f"Enforcement for {target.display_name} has been updated.")
    reply.add_field(name = "Former identity:", value = former_identity.name)
    reply.add_field(name = "New identity:", value = "Themselves")
    reply.set_footer(text = random.choice(text.identity_release))

    await context.send(embed=reply)

@bot.command(aliases = ['yoink'])
async def clone(context, target, identity_name):
    logger.info("Clone command triggered.")

    if target is None or identity_name is None:
        return

    #Check user does not already have an ID with the given name
    #Query DB for IDs beloning to target user with specified name,
    #If exists, insert duplicate entry into DB where owner ID = message author ID

@bot.command(aliases = ['assume-direct-control', 'puppeteer', "amplify"])
async def puppet(context, target: discord.Member, message):
    relationship = db.get_relationship(context.author, target)
    if relationship is None:
        # Not domming.
        return
    elif relationship.confirmed != 1:
        # Also not domming.
        return
    
    webhook = await get_webhook(context.channel)
    await webhook.send(message, username=target.display_name, avatar_url=target.avatar_url)


#Events
@bot.event
async def on_ready():
    logger.info("Identity Enforcement Drone #3161 online.")
    game = discord.Game("with your identity.")
    await bot.change_presence(activity = game)

@bot.event
async def on_message(message):

    #Don't deal with bots.
    if message.author.bot: 
        return

    #Check the db to see if the user is enforced in the guild
    #If yes, enforce.
    if (enforcement := db.get_enforcement(message.author, message.guild)) is not None:
        logger.info(f"Enforcing {message.author.name} with identity of ID {enforcement.identity_id}")
        await en.enforce_user(message, enforcement)

    if message.content.lower().startswith("beep"):
        await message.channel.send("Boop!")
        logger.info(f"{message.author.display_name} beeped! I booped back.")

    if message.content.lower().startswith("boop"):
        await message.channel.send("Beep!")
        logger.info(f"{message.author.display_name} booped! I beeped back.")

    if message.content.lower() in ["good bot", "good bot!", "goo    d bot."]:
        logger.info(f"{message.author.display_name} called me a good bot! ///")
        await message.channel.send("Y-You too... <3")
    
    await bot.process_commands(message)

@bot.event
async def on_command_error(context, error):
    logger.error(f"!!! --- EXCEPTION CAUGHT IN {context.command} COMMAND --- !!!")
    logger.error(error)
    with open("log.txt", "a") as exception_file:
        traceback.print_exception(type(error), error, error.__traceback__, file=exception_file) #Prints to file for logging
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr) #Prints to console for debugging
    logger.info("!!! --- End exception log. --- !!!")

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f'!!! --- EXCEPTION CAUGHT IN {event} --- !!!')
    with open("log.txt", "a") as exception_file:
        traceback.print_exc(file=exception_file)
    traceback.print_exc()
    logger.info("!!! --- End exception log. --- !!!")

logger.info("Doing data migration.")
db.migration()
logger.info("Data migration done.")

logger.info("Starting up Identity Enforcement Drone #3161.")
bot.run(bot_token)
