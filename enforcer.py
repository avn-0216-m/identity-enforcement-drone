#import core modules
import sys
import discord
from discord.ext import commands
import json
import mysql.connector

#import handler modules
from relationship import Relationship_Handler
from database import Database_Handler
#import utility modules 
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

@bot.command()
async def db_reset(context):
    if db.completely_reset_database():
        await context.send("`I hope you're proud of yourself.`")

@bot.command()
async def db_push(context, argument):
    if db.add_message(argument, context.message.author.id):
        await context.send("`Your message was succesfully added to the database. :)`")


@bot.command()
async def db_list(context):
    print("Listing all entries in database")
    output_message = "```"
    for message_id, user_id, message in db.get_recent_from_table(MESSAGES, "message_id"):
        user_from_id = bot.get_user(int(user_id))
        user_name = f"{user_from_id.name}#{user_from_id.discriminator}"
        output_message += f'Message {message_id}: "{message}" by {user_name}\n'
    output_message += "```"
    await context.send(output_message if output_message != "``````" else "`No messages found.`")

@bot.command()
async def dominate(context, argument):
    if rl.handle_dominate_query():
        await context.send("`Hey, good job kiddo, you dominated somebody (not really).`")
    

@bot.event
async def on_ready():
    print("Identity Enforcement Drone #3161 ready.")

print("Starting bot.")
bot.run(bot_token)