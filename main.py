#!/usr/bin/python

#import core modules
import sys
import discord
import logging
from discord.ext import commands
import json
import mysql.connector
import asyncio

#import handler modules
from relationship import Relationship_Handler
from database import Database_Handler
from enforcement import Enforcement_Handler
#import utility modules 
from notable_entities import ENFORCEMENT_PREFIX, ENFORCEMENT_DRONE
from utils import scrape_drone_id
#import data structure modules
from database_constants import DATABASE_NAME, MESSAGES
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
with open("secret_details.json") as secret_file:
    secret_details = json.load(secret_file)
    db_host = secret_details['db_host']
    db_user = secret_details['db_user']
    db_pass = secret_details['db_pass']
    bot_token = secret_details['bot_token']
logger.info("Secret details successfully loaded.")

db = Database_Handler(db_host, db_user, db_pass)
rl = Relationship_Handler(db)
en = Enforcement_Handler(bot, db)

async def cull_roles():

    do_not_cull = []
    total_culled = 0

    while True:
        await asyncio.sleep(60 * 60 * 24) #60 * 60 * 24 = 24 hours
        logger.info("Beginning routine role cull on all available servers.")
        for guild in bot.guilds:
            for member in guild.members:
                for role in member.roles:
                    if role.name.startswith(ENFORCEMENT_PREFIX):
                        do_not_cull.append(role)
            for role in guild.roles:
                if role not in do_not_cull and role.name.startswith(ENFORCEMENT_PREFIX):
                    logger.info(f'Culling enforcement role "{role.name[3:]}" in guild "{guild.name}"')
                    total_culled += 1
                    await role.delete()
            logger.info(f'Culled {total_culled} roles in "{guild.name}"')

        do_not_cull.clear()


# @bot.command()
# async def db_reset(context):
    # if db.completely_reset_database() is Status.OK:
        # await context.send("I hope you're proud of yourself.")

@bot.command()
async def db_push(context, argument):
    if db.add_message(argument, context.message.author.id) is Status.OK:
        logger.info(f'{context.message.author.display_name} added the message "{argument}" to the database.')
        await context.send("Your message was succesfully added to the database. :)")

@bot.command()
async def db_list(context):
    logger.info("Listing all messages in the database.")
    output_message = ""
    for message_id, user_id, message in db.get_recent_from_table(MESSAGES, "message_id", "10"):
        user_from_id = bot.get_user(int(user_id))
        user_name = f"{user_from_id.name}#{user_from_id.discriminator}"
        output_message += f'Message {message_id}: "{message}" by {user_name}\n'
    await context.send(output_message if output_message != "" else "No messages found.")

@bot.command(aliases = ['dom'])
async def dominate(context, submissive: discord.Member):
    '''
    Attempt to dominate someone
    They must respond by submitting to you with the submit command.
    '''

    logger.info(f'{context.message.author.display_name} is trying to dominate {submissive.display_name}')

    if context.message.author is submissive:
        await context.send("You cannot own yourself.")
        return

    if submissive.id == ENFORCEMENT_DRONE:
        await context.send("Thanks, but no thanks.")
        return

    response = rl.handle_dominate_query(context.message.author, submissive)
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

    logger.info(f'{context.message.author.display_name} is trying to submit to {dominant.display_name}')

    if context.message.author is dominant:
        await context.send("You cannot submit to yourself.")
        return

    if dominant.id == ENFORCEMENT_DRONE:
        await context.send("Thanks, but no thanks.")
        return

    response = rl.handle_submit_query(context.message.author, dominant)
    if response is Status.DUPLICATE_REQUEST:
        await context.send("You are already submissive to/attempting to submit to that person. You needy fucking bottom, chill out.")
    elif response is Status.OK:
        await context.send("Get ready to keysmash in delight- your request to submit has been received. Now the other party simply needs to dominate you in turn.")
    elif response is Status.HOLY_MATRIHORNY:
        await context.send("By the power invested in my processor, I now pronounce you dom and sub. Huzzah!")
    
@bot.command()
async def list(context, arg1: str = None, arg2: str = None):

    logger.info(f"{context.message.author.display_name} has requested to list something.")

    if arg1 is None:
        await context.send("What would you like to list?")
        return
    elif arg1 == "submissives" or arg1 == "subs":
        results = db.get_all_submissives(context.message.author.id).data
        reply = "On this server, you own the following submissives:\n"

        subs_in_other_servers = 0

        for result in results:
            sub_as_user = bot.get_user(int(result.submissive_id))
            if sub_as_user is not None:
                reply += f"{sub_as_user.name}\n"
            else:
                subs_in_other_servers += 1
        plural = ("sub" if subs_in_other_servers == 1 else "subs")
        reply += f"...and {subs_in_other_servers} {plural} elsewhere on Discord~\n"
        if len(reply) > 2000:
            reply = "You own too many submissives to count. Well done."
        await context.send(reply)
    elif arg1 == "server":
        identities = db.get_all_identities_for_guild(context.guild.id).data
        if len(identities) == 0:
            await context.send("This server hosts no identities.")
            return
        reply = "This server hosts the following identities:\n"
        for identity in identities:
            if identity.display_name == None and identity.display_name_with_id == None:
                reply += f'"{identity.name}",'
            elif identity.display_name == None:
                reply += f'"{identity.name}", with the display name "{identity.display_name_with_id}" if you\'re a drone.\n'
            elif identity.display_name_with_id == None:
                reply += f'"{identity.name}", with the display name "{identity.display_name}"\n'
            else:
                reply += f'"{identity.name}, with the display name "{identity.display_name}" or {identity.display_name} if you\'re a drone.\n'
        await context.send(reply)
    elif arg1 == "my":
        identities = db.get_all_identities_for_user(context.message.author.id).data
        if len(identities) == 0:
            await context.send("You possess no identities right now. Kinda hot! Why not make one?")
            return
        reply = "You own the following identities:\n"
        for identity in identities:
            reply += f'"{identity.name}",\n'

@bot.command()
async def set(context, arg1: str = None, arg2 = None):

    '''
    Set a wide array of parameters with this function.
    '''
    if arg1 is None:
        await context.send("What would you like to set?")
        return
    elif arg1 == "command_channel":
        await context.send("cool beanzo")
    
@bot.command()
async def register(context):
    if db.get_registered_user(context.message.author.id).data != []:
        await context.send("You're already registered.")
        return

    drone_id = scrape_drone_id(context.message.author.display_name)

    if drone_id is not None:
        db.register_user_with_id(context.message.author.id, drone_id)
        await context.send("We've registered you in the database- and I couldn't help but notice your cute little drone ID, so we've made a note of that too. <3")
        return

    db.register_user(context.message.author.id)
    await context.send("You've been registered in our database. :)")

@bot.command()
async def refresh(context):
    logger.info(f"Refreshing default identities for server: {context.guild}")
    en.refresh_default_identities(context.guild)
    await context.send("Default identities for this server have been refreshed.")

@bot.command(aliases = ['assign'])
async def enforce(context, arg1: discord.Member, arg2: str):
    '''
    Assign an identity role to a user.
    '''
    print("Enforcing.")

    if not en.check_permissions(context.message.author.id, arg1.id):
        await context.send("You cannot enforce users who are not submissive to you.")
        return

    status = await en.assign(arg1, arg2)
    if status is Status.OK:
        await context.send("Identity assigned.")
    elif status is Status.BAD_REQUEST:
        await context.send("Not a valid identity. See server identities by typing 'list identities'")

@bot.command()
async def release(context, arg: discord.Member):
    for role in arg.roles:
        if role.name.startswith(ENFORCEMENT_PREFIX):
            print("Enforcable role found. Removing.")
            await arg.remove_roles(role)
            await context.send("Enforcable identity removed.")
            return
    await context.send("That user does not have an assigned identity.")

@bot.event
async def on_ready():
    print("Identity Enforcement Drone #3161 ready.")
    global culling_roles
    if not culling_roles:
        culling_roles = True
        asyncio.ensure_future(cull_roles())

@bot.command()
async def id(context):
    if scrape_drone_id(context.message.author.display_name) is not None:
        await context.send("But... You're _already_ a good little drone, sweetie!")
        return
    generated_id = en.generate_new_id(context.guild)
    try:
        await context.message.author.edit(nick=generated_id)
        await context.send(f"Your wonderful new drone ID is {generated_id}! I've went ahead and assigned it to you- I know you're probably very eager to be a good drone! Enjoy.")
    except discord.errors.Forbidden:
        await context.send(f"Your wonderful new drone ID is {generated_id}! I would've assigned it to you, but you rank higher than me, so I can't change your nickname.")

@bot.event
async def on_message(message):

    #Don't deal with bots.
    if message.author.bot: 
        return

    #Check if any user roles begin with '🟆:' (Which marks an enforcable role)
    for role in message.author.roles:
        if role.name.startswith('🟆: '):
            await en.enforce(message=message, role=role)

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

print("Starting bot.")
bot.run(bot_token)
