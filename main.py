import json
import discord
from discord.ext import commands
import asyncio

from commands.Music import Music
from commands.RiotGamesAPI import RiotGamesAPI

intents = discord.Intents.default()
intents.members = True
prefix = "!"

bot = commands.Bot(command_prefix=prefix, intents=intents)

f = open('config.json','r')
config = json.loads(f.read())
f.close()

@bot.event
async def on_ready():
    bot.add_cog(Music(bot))
    bot.add_cog(RiotGamesAPI(bot, config['riot-api']))
    print("Logged in as {0.user}".format(bot))
    print("\twith client id {0.user.id}".format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="my prefix is " + prefix))

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    can_delete = False
    try:
        can_delete = bot.user.permissions_in(ctx.channel).manage_messages
    except:
        print("Probably no user perms established yet, not deleting messages.")
        print("\tMessage ID:", ctx.message.id)
        print("\tGuild ID:", ctx.guild.id)
        print("\tTimestamp:", ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    await ctx.channel.send(str(int(round(bot.latency * 1000,0))) + " ms", delete_after=15 if can_delete else None)
    if can_delete:
        await asyncio.sleep(15)
        await ctx.message.delete()

@bot.command()
async def github(ctx):
    can_delete = False
    try:
        can_delete = bot.user.permissions_in(ctx.channel).manage_messages
    except:
        print("Probably no user perms established yet, not deleting messages.")
        print("\tMessage ID:", ctx.message.id)
        print("\tGuild ID:", ctx.guild.id)
        print("\tTimestamp:", ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    await ctx.channel.send("See me on GitHub! https://github.com/zeuschops/idea-train", delete_after=10 if can_delete else None)
    if can_delete:
        await asyncio.sleep(10)
        await ctx.message.delete()

@bot.command()
async def invite(ctx):
    can_delete = False
    try:
        can_delete = bot.user.permissions_in(ctx.channel).manage_messages
    except:
        print("Probably no user perms established yet, not deleting messages.")
        print("\tMessage ID:", ctx.message.id)
        print("\tGuild ID:", ctx.guild.id)
        print("\tTimestamp:", ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    await ctx.channel.send("Invite me to your server! https://discord.com/oauth2/authorize?client_id=799451713735622666&scope=bot&permissions=309668928", delete_after=10 if can_delete else None)
    if can_delete:
        await asyncio.sleep(10)
        await ctx.message.delete()

@bot.command()
async def clean(self, ctx, count:int):
    user_perms = ctx.message.author.permissions_in(ctx.channel)
    if user_perms.administrator or user_perms.manage_messages:
        await ctx.channel.purge(limit=count)
        await ctx.send("Deleted " + str(count) + " messages", delete_after=10)
    else:
        await ctx.send("You do not have permission to use this command.", timeout=15)

@commands.command()
async def checkrainVersion(self, ctx):
    home_req = requests.get('https://checkra.in')
    link_idx = str(home_req.content)[2:-1].index('href="/releases/')
    link_str = str(home_req.content)[link_idx + 2 + len('href="'):]
    link_str = link_str[:link_str.index('">')]
    version_str = link_str.split('/')[-1]
    download_req = requests.get('https://checkra.in' + link_str)
    download_idx = str(download_req.content)[2:-1].index('href="https://assets.checkra.in/')
    download_str = str(download_req.content)[2 + download_idx + len('href="'): -1]
    download_str = download_str[:download_str.index('" ')]
    await ctx.channel.send('The current checkra1n version is: ' + version_str + '. The latest download link (for Mac) is: <' + download_str + '>')

bot.run(config['token'], bot=True)
