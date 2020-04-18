#import core modules
import sys
import discord
from discord.ext import commands
import json
import mysql.connector
#import enforcer modules
#import utility modules 
#import data structure modules

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
print("Establishing connection with database.")
database = mysql.connector.connect(host=db_host, user=db_user, passwd=db_pass)
print(database)
print("Connection established.")
print("Starting bot.")
bot = commands.Bot(command_prefix="//")
bot.run(bot_token)

@bot.command()
async def reset(context):
    print("Resetting database.")

@bot.command()
async def push(context, argument):
    print("Pushing argument to database.")

@bot.command()
async def list(context, argument):
    print("Listing entries in database")