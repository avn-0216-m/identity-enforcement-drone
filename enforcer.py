#import core modules
import sys
import discord
from discord.ext import commands
import json
import mysql.connector
#import enforcer modules
#import utility modules 
#import data structure modules
from database_constants import DATABASE_NAME, TEST_TABLE_NAME

bot = commands.Bot(command_prefix="")

@bot.command()
async def db_reset(context):
    print("Resetting database.")
    cursor.execute("DROP DATABASE IF EXISTS " + DATABASE_NAME)
    print("Database dropped.")
    cursor.execute("CREATE DATABASE " + DATABASE_NAME)
    print("Database created.")
    cursor.execute("USE " + DATABASE_NAME)
    cursor.execute("CREATE TABLE " + TEST_TABLE_NAME + "(message_id int not null primary key auto_increment, message varchar(255))")
    print("Test table created.")
    await context.send("Database reset.")

@bot.command()
async def db_push(context, argument):
    print("Pushing argument to database.")
    print(f'INSERT INTO {DATABASE_NAME}.{TEST_TABLE_NAME}(message) VALUE("{argument}");')
    cursor.execute(f'INSERT INTO {DATABASE_NAME}.{TEST_TABLE_NAME}(message) VALUE("{argument}");')
    await context.send("Message '" + argument + "' added to the database.")

@bot.command()
async def db_list(context):
    print("Listing all entries in database")
    for entry in cursor.execute(f"SELECT * FROM {TEST_TABLE_NAME}"):
        print(dir(entry))
        print(entry)

@bot.event
async def on_ready():
    print("Bot ready. Creating database if it doesn't already exist.")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    cursor.execute(f"USE {DATABASE_NAME}")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {TEST_TABLE_NAME} (message_id int not null primary key auto_increment, message varchar(255))")
    print("Database ready.")

#Main setup begins here.
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
print("Setting database autocommit to true.")
database.autocommit= True
cursor = database.cursor()
print("Starting bot.")
bot.run(bot_token)