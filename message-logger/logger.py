import discord
from discord.ext import commands
import json
import mariadb

f = open('../config.json','r')
config = json.loads(f.read())
f.close()

bot = commands.Bot(command_prefix='??')

db = mariadb.connect(user=config['db']['user'], password=config['db']['password'], database=config['db']['database'])
cursor = db.cursor()

@bot.event
async def on_ready():
    print("Logged in as", "%s#%i" % (bot.user.name, bot.user.id))

@bot.event
async def on_message(message):
    timestr = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
    author = {
        "id": message.author.id,
        "name": message.author.name,
        "nick": message.author.nick,
        "dicrim":message.author.discriminator,
        "created_at":message.author.created_at,
        "joined_at":message.author.joined_at
    }
    guild = {
        "id":message.guild.id,
        "name":message.guild.name,
        "owner_id":message.guild.owner_id
    }
    channel = {
        "id":message.channel.id,
        "name":message.channel.name
    }
    cursor.execute("SELECT * FROM users WHERE id=%f" % author['id'])
    data = cursor.fetchall()
    if len(data) == 0:
        cursor.execute("INSERT INTO users() VALUES ();")
    await bot.process_commands(message)

bot.run(config['token'])