#import core
import discord
import sys
import json
#import modules
#import utility
#import data structures

bot = discord.ext.commands.Bot(command_prefix='//', case_insensitive=True)
print("Getting SQL details")
with open("sql_details.json") as sql_file:
    sql_details = json.load(sql_file)
    for detail in details:
        print(detail)
        
bot.run(sys.argv[1])

@bot.command()
async def reset(context):
    print("Resetting database.")

@bot.command()
async def push(context, argument):
    print("Pushing argument to database.")

@bot.command()
async def list(context, argument):
    print("Listing entries in database")