import json
import discord
from discord.ext import commands
from commands.VersionRequests import VersionRequests

bot = commands.Bot(command_prefix="??")

f = open('config.json','r')
config = json.loads(f.read())
f.close()

@bot.event
async def on_ready():
    bot.add_cog(VersionRequests(bot))
    print("Logged in as {0.user}".format(bot))
    print("\twith client id {0.user.id}".format(bot))

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.channel.send(str(int(round(bot.latency * 1000,0))) + " ms")

bot.run(config['token'], bot=True, reconnect=True)