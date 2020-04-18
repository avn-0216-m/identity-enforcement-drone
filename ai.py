#import core
import discord
import sys
#import modules
#import utility
#import data structures

bot = discord.ext.commands.Bot(command_prefix='//', case_insensitive=True)
print("Starting bot!")
bot.run(sys.argv[1])