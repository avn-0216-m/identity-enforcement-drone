#import core modules
import sys
import discord
from discord.ext import commands
import json
import mysql.connector

#import handler modules
from relationship import Relationship_Handler
from database import Database_Handler
from enforcement import Enforcement_Handler
#import utility modules 
from notable_entities import ENFORCEMENT_PREFIX, ENFORCEMENT_DRONE
#import data structure modules
from database_constants import DATABASE_NAME, MESSAGES
from data_classes import Status

bot = commands.Bot(command_prefix="!")

print("Getting SQL and token details")
with open("secret_details.json") as secret_file:
    secret_details = json.load(secret_file)
    for key in secret_details:
        print("--------------")
        print(key)
        print(secret_details[key])
    db_host = secret_details['db_host']
    db_user = secret_details['db_user']
    db_pass = secret_details['db_pass']
    bot_token = secret_details['bot_token']

db = Database_Handler(db_host, db_user, db_pass)
rl = Relationship_Handler(db)
en = Enforcement_Handler(bot, db)

@bot.command()
async def db_reset(context):
    if db.completely_reset_database() is Status.OK:
        await context.send("I hope you're proud of yourself.")

@bot.command()
async def db_push(context, argument):
    if db.add_message(argument, context.message.author.id) is Status.OK:
        await context.send("Your message was succesfully added to the database. :)")

@bot.command()
async def db_list(context):
    print("Listing all entries in database")
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
async def list(context, arg: str = None):
    if arg is None:
        await context.send("What would you like to list?")
        return
    elif arg == "submissives" or arg == "subs":
        results = db.get_all_submissives(context.message.author.id).data
        reply = "You currently own the following submissives:\n"
        for result in results:
            sub_as_user = bot.get_user(int(result.submissive_id))
            reply += f"* {sub_as_user.name}#{sub_as_user.discriminator}\n"
        if len(reply) > 2000:
            reply = "You own too many submissives to count. Well done."
        await context.send(reply)
    elif arg == "identities":
        identities = db.get_all_identities_for_guild(context.guild.id).data
        if len(identities) == 0:
            await context.send("This server hosts no identities.")
            return
        reply = "This server hosts the following identities:\n"
        for identity in identities:
            reply += f"[{identity.name}], with the display name [{identity.display_name}]\n"
        await context.send(reply)

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
    

@bot.command()
async def refresh(context):
    print("Refreshing command triggered.")
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

@bot.event
async def on_message(message):

    #Don't deal with bots.
    if message.author.bot: 
        return

    #Check if any user roles begin with '🟆:' (Which marks an enforcable role)
    for role in message.author.roles:
        if role.name.startswith('🟆: '):
            await en.enforce(message=message, role=role)
    await bot.process_commands(message)

print("Starting bot.")
bot.run(bot_token)