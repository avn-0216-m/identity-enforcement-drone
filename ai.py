#import core
import discord
import sys
#import modules
#import utility
#import data structures

bot = discord.ext.commands.Bot(command_prefix='//', case_insensitive=True)
print("Starting bot!")
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