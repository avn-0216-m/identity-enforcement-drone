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
from notable_entities import ENFORCEMENT_PREFIX, ENFORCEMENT_DRONE, ALLOWED_ATTRIBUTES_AND_COMMANDS, ALLOWED_MODES
import text
#import data structure modules
from data_classes import Status
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


#on_ready checkers
culling_roles = False

bot = commands.Bot(command_prefix="!", case_insensitive=True)

logger.info("Loading secret details from file.")
with open("bot_token.txt") as secret_file:
    bot_token = secret_file.readline()

#Initalize DAO
db = Database()

#Commands
@bot.command(aliases = ['dom'])
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

@bot.command(aliases = ['sub'])
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

@bot.command(aliases = ['yeet', 'uncollar', 'goodbye'])
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

    await context.send(embed = reply)
    
@bot.command(aliases = ['init'])
async def defaults(context):
    db.set_default_identities(context.message.author)
    reply = discord.Embed(title = f"Identities added for {context.message.author.display_name}:")
    for identity in DEFAULT_IDENTITIES:
        reply.add_field(inline = False, name = identity.name, value = identity.description)
    await context.send(embed = reply)

@bot.command(aliases = ['assign'])
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

@bot.command()
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

@bot.command(aliases = ['id', 'identities', 'ids', 'idsnuts'])
async def identity(context, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
    #This is the big boy command, the real fat schmeat of the program.
    #Here's a fucken docstring for ya:
    #arg1: An identity name.
    #arg2: Either an identity attribute (name/desc/lexicon/etc) or a command (new/rename/delete)
    #arg3: The new value for the attribute specified in arg2
    #arg4: Optional mode for value setting (replace/append/delete)

    #List another users identities if they are mentioned.
    if context.message.mentions != []:
        logger.info("Listing all identities belonging to mentioned users.")

        reply = discord.Embed()

        for user in context.message.mentions:
            logger.info(f"Getting identities for {user.name}")
            #Get all IDs belonging to mentioned user and append their name + description

            identities = db.get_all_user_identities(user)

            id_text = ""
            for identity in identities:
                id_text += f"**{identity.name}**"
                if identity.description is not None:
                    id_text += f': "{identity.description}"'
                id_text += "\n"
            if id_text != "":
                reply.add_field(name = user.display_name, value = id_text, inline = False)
        await context.send(embed=reply)
        return

    #Validate that they've given an identity name.
    elif arg1 is None:

        #TODO: This is a temporary way to list self owned identities. Delete later.
        reply = discord.Embed()
        identities = db.get_all_user_identities(context.author)
        id_text = ""
        for identity in identities:
            id_text += f"**{identity.name}**"
            if identity.description is not None:
                id_text += f': "{identity.description}"'
            id_text += "\n"
        if id_text != "":
            reply.add_field(name = context.author.display_name, value = id_text, inline = False)
        await context.send(embed=reply)
        return

    #TODO: Delete this when identity command is finished.
    else:
        await context.send("Sorry, you can't make new commands yet. Initialize the defaults with the `!default` command.")
        return

    identity = db.get_user_identity_by_name(context.message.author.id, arg1)

    #Validate that the identity name is valid.
    if identity is None: #No matching identities were found
        if arg2.lower() == "new":
            logger.info("Creating new identity.")
        else:
            logger.info("Invalid identity name given.")

    #Validate attribute/command.
    if arg2.lower() not in ALLOWED_ATTRIBUTES_AND_COMMANDS:
        logger.info("Invalid attribute/command specified.")

    #Validate mode.
    if arg4.lower() not in ALLOWED_MODES:
        logger.info("Invalid mode specified.")


@bot.command(aliases = ['yoink'])
async def clone(context, target, identity_name):
    logger.info("Clone command triggered.")

    if target is None or identity_name is None:
        return

    #Check user does not already have an ID with the given name
    #Query DB for IDs beloning to target user with specified name,
    #If exists, insert duplicate entry into DB where owner ID = message author ID

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

    if message.content.lower() in ["good bot", "good bot!", "good bot."]:
        logger.info(f"{message.author.display_name} called me a good bot! ///")
        await message.channel.send("Y-You too... <3")
    
    await bot.process_commands(message)

@bot.event
async def on_command_error(context, error):
    logger.error(f"!!! --- Exception caught in {context.command} command --- !!!")
    logger.error(error)
    exception_file = open("log.txt", "a")
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr) #Prints to console for debugging
    traceback.print_exception(type(error), error, error.__traceback__, file=exception_file) #Prints to file for logging
    exception_file.close()
    logger.info("!!! --- End exception log. --- !!!")

logger.info("Doing data migration.")
db.migration()
logger.info("Data migration done.")

logger.info("Starting up Identity Enforcement Drone #3161.")
bot.run(bot_token)
