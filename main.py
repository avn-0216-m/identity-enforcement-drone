#!/usr/bin/python

#import core modules
import sys
import discord
import logging
from discord.ext import commands
import json
import mysql.connector
import asyncio
import random
import traceback

#import handler modules
from relationship import Relationship_Handler
from database import Database_Handler
from enforcement import Enforcement_Handler
#import utility modules 
from notable_entities import ENFORCEMENT_PREFIX, ENFORCEMENT_DRONE, ALLOWED_ATTRIBUTES_AND_COMMANDS, ALLOWED_MODES
from utils import scrape_drone_id
#import data structure modules
from data_classes import Status

#Setup logger
logger = logging.getLogger('Identity Enforcement Drone')
formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d :: %(levelname)s :: %(message)s', datefmt='%Y-%m-%d :: %H:%M:%S')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
fh = logging.FileHandler('log.txt')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

logger.info("-----------------------------------------------")
logger.info("It's a new day~!")
logger.info("-----------------------------------------------")


#on_ready checkers
culling_roles = False

bot = commands.Bot(command_prefix="!", case_insensitive=True)

logger.info("Loading secret details from file.")
with open("bot_token.txt") as secret_file:
    bot_token = secret_file.readline()

db = Database_Handler()
rl = Relationship_Handler(db)
en = Enforcement_Handler(bot, db)

#Utility Methods
async def cull_roles():

    do_not_cull = []
    total_culled = 0

    while True:
        await asyncio.sleep(60 * 60 * 24) #60 * 60 * 24 = 24 hours
        for guild in bot.guilds:
            total_culled = 0
            for member in guild.members:
                for role in member.roles:
                    if role.name.startswith(ENFORCEMENT_PREFIX):
                        do_not_cull.append(role)
            for role in guild.roles:
                if role not in do_not_cull and role.name.startswith(ENFORCEMENT_PREFIX):
                    logger.info(f'Culling unused enforcement role "{role.name[3:]}" in guild "{guild.name}"')
                    total_culled += 1
                    await role.delete()
            if total_culled > 0: 
                logger.info(f'Culled {total_culled} roles in "{guild.name}"')

        total_culled = 0
        do_not_cull.clear()

#Commands
@bot.command(aliases = ['dom'])
async def dominate(context, submissive: discord.Member):
    '''
    Attempt to dominate someone
    They must respond by submitting to you with the submit command.
    '''

    if submissive is not discord.Member: return #Bad request!!

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
    elif response is Status.OK:
        await context.send("Request to dominate recieved. The sub will need to submit to you with the 'submit' command.")
    elif response is Status.HOLY_MATRIHORNY:
        await context.send("By the power invested in my hard drive, I now pronounce you sub and dom. Hurray!")

@bot.command(aliases = ['sub'])
async def submit(context, dominant: discord.Member):
    '''
    Attempt to submit to someone
    They must respond by dominating you with the dominate command.
    '''

    if dominant is not discord.Member: return

    logger.info(f'{context.message.author.display_name} is trying to submit to {dominant.display_name}')

    if context.message.author is dominant:
        await context.send("You cannot submit to yourself.")
        return

    if dominant.id == ENFORCEMENT_DRONE:
        await context.send("Thanks, but no thanks.")
        return

    response = rl.handle_relationship_query(context.message.author, dominant, context.message.author)
    if response is Status.DUPLICATE_REQUEST:
        await context.send("You are already submissive to/attempting to submit to that person. You needy fucking bottom, chill out.")
    elif response is Status.OK:
        await context.send("Get ready to keysmash in delight- your request to submit has been received. Now the other party simply needs to dominate you in turn.")
    elif response is Status.HOLY_MATRIHORNY:
        await context.send("By the power invested in my processor, I now pronounce you dom and sub. Huzzah!")
    

    logger.info(f"{context.message.author.display_name} has requested to list something.")

@bot.command(aliases = ['yeet', 'relenquish'])
async def uncollar(context, arg: discord.Member = None):
    if arg is None:
        #Reprimand user for not tagging someone.
        return
    #Check if they have a relationship with the user here and delete it if true.

@bot.command(aliases = ['assign'])
async def enforce(context, target: discord.Member, identity: str):
    '''
    Assign an identity role to a user.
    '''

    #Validate args
    if target is not discord.Member or identity is not str: return

    logger.info(f"Enforcement command triggered. {context.message.author.name} wants to enforce {target.name} with the identity {identity} in {context.guild.name}")

    #Confirm the user has the specified identity

    if db.get_user_identity_by_name(context.message.author, identity) is None:
        await context.send("You do not have that specified identity.")
    else:
        await context.send("Right away baws!")

    #Confirm the user is domming the target
    #Insert an enforcement record in the enforcement table with the victim id, guild id, and the identity id.

@bot.command()
async def release(context, arg: discord.Member):
    logger.info(f"Release command triggered. {context.message.author.name} wants to release {arg.name} in {context.guild.name}")

    #Delete from Enforcements table where user_id = mention.id and guild_id = guild id

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
                id_text += identity.name
                if identity.description is not None:
                    id_text += f': "{identity.description}"'
                id_text += "\n"
            if id_text != "":
                reply.add_field(name = user.display_name, value = id_text, inline = False)
        await context.send(embed=reply)
        return
    
    #Validate that they've given an identity name.
    elif arg1 is None:
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
    global culling_roles
    if not culling_roles:
        culling_roles = True
        asyncio.ensure_future(cull_roles())

    game = discord.Game("with your identity.")
    await bot.change_presence(activity = game)

@bot.event
async def on_message(message):

    #Don't deal with bots.
    if message.author.bot: 
        return

    #Check the db to see if the user is enforced in the guild
    #If yes, enforce.

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
