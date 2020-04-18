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
from data_classes import Status
#import data structure modules
from database_constants import DATABASE_NAME, MESSAGES

bot = commands.Bot(command_prefix="")

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
en = Enforcement_Handler(bot)

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
    Attempt to dominate someone.
    They must respond by submitting to you with the submit command.
    '''
    response = rl.handle_dominate_query(context.message.author, submissive)
    print("Response is:")
    print(response)
    if response is Status.DUPLICATE_REQUEST:
        await context.send("You are already dominating/attempting to dominate that person.")
    elif response.status is Status.OK:
        plural = "user" if response.data == 1 else "users"
        await context.send("You are now dominating " + submissive.mention + f"\nIn total, you are dominating {response.data} {plural}.")
    
@bot.command()
async def list(context, arg: str = None):
    if arg is None:
        await context.send("What would you like to list?")
        return
    if arg == "submissives" or "subs":
        subs = rl.get_all_submissives(context.message.author).data
        reply = "You currently own the following submissives:\n"
        for sub_id, in subs: #The comma is to unpack a tuple with only 1 value (super weird)
            sub_as_user = bot.get_user(int(sub_id))
            reply += f"* {sub_as_user.name}#{sub_as_user.discriminator}\n"
        if len(reply) > 2000:
            reply = "You own too many submissives to count. Well done."
        await context.send(reply)

@bot.event
async def on_ready():
    print("Identity Enforcement Drone #3161 ready.")

@bot.event
async def on_message(message):

    if message.author.bot: #Don't deal with bots.
        return

    print("Message incoming.")
    #Check if any user roles begin with '🟆:' (Which marks an enforcable role)
    for role in message.author.roles:
        if role.name.startswith('🟆: '):
            print("Enforcable role found.")
            en
    return

print("Starting bot.")
bot.run(bot_token)