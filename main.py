import json
import discord
from discord.ext import commands
import asyncio

from commands.AdministratorCommands import AdministratorCommands
from commands.VersionRequests import VersionRequests
from commands.Music import Music
#from commands.WGUCourses import WGUCourses
from commands.RiotGamesAPI import RiotGamesAPI

bot = commands.Bot(command_prefix="!")

f = open('config.json','r')
config = json.loads(f.read())
f.close()

@bot.event
async def on_ready():
    bot.add_cog(Music(bot))
    bot.add_cog(VersionRequests(bot))
    bot.add_cog(AdministratorCommands(bot))
    bot.add_cog(WGUCourses(bot))
    bot.add_cog(RiotGamesAPI(bot, config['riot-api']))
    print("Logged in as {0.user}".format(bot))
    print("\twith client id {0.user.id}".format(bot))
    #await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="My prefix is now !"))

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.channel.send(str(int(round(bot.latency * 1000,0))) + " ms", delete_after=15)
    await asyncio.sleep(15)
    await ctx.message.delete()

@bot.command()
async def github(ctx):
    await ctx.channel.send("See me on GitHub! https://github.com/zeuschops/ideal-train", delete_after=10)
    await asyncio.sleep(10)
    await ctx.message.delete()

@bot.command()
async def invite(ctx):
    await ctx.channel.send("Invite me to your server! https://discord.com/oauth2/authorize?client_id=799451713735622666&scope=bot&perms=309668928", delete_after=10)
    await asyncio.sleep(10)
    await ctx.message.delete()

bot.run(config['token'], bot=True, reconnect=True)