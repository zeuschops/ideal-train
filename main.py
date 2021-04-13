import json
import discord
from discord.ext import commands
import asyncio
import os

from commands.AdministratorCommands import AdministratorCommands
from commands.VersionRequests import VersionRequests
from commands.Music import Music
from commands.WGUCourses import WGUCourses
from commands.RiotGamesAPI import RiotGamesAPI
#from commands.TempCommands import TempCommands

intents = discord.Intents.default()
intents.members = True
prefix = "!"

activity_data = {}
if 'activity-data.json' in os.listdir('helpers/'):
    f = open('helpers/activity-data.json','r')
    activity_data = json.loads(f.read())
    f.close()

bot = commands.Bot(command_prefix=prefix, intents=intents)

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
    #bot.add_cog(TempCommands(bot))
    print("Logged in as {0.user}".format(bot))
    print("\twith client id {0.user.id}".format(bot))
    #await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="My prefix is !"))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="my prefix is " + prefix))

@bot.event
async def on_message(message):
    if '!bubo ' not in message.content:
        await bot.process_commands(message)
    if 'message' not in list(activity_data):
        activity_data.update({'message':{}})
    if str(message.guild.id) not in list(activity_data['message']):
        activity_data['message'].update({
            str(message.guild.id):{
                str(message.id):{
                    "author":{
                        "id":message.author.id,
                        "name":message.author.name,
                        "discrim":message.author.discriminator,
                        "nickname":message.author.nick
                    },
                    "content":message.content,
                    "embeds":[
                        {
                            "url":embed.url,
                            "title":embed.title,
                            "color":embed.colour,
                            "description":embed.description,
                            "fields":[
                                {
                                    "title":field.title,
                                    "description":field.description
                                } for field in embed.fields
                            ],
                            "thumbnail":embed.thumbnail,
                            "footer":embed.footer
                        } for embed in message.embeds
                    ],
                    "timestamp":message.created_at
                }
            }
        })
    else:
        activity_data['message'][str(message.guild.id)].update({
            str(message.id): {
                "author": {
                    "id":message.author.id,
                    "name":message.author.name,
                    "discrim":message.author.discriminator,
                    "nickname":message.author.nick
                },
                "content":message.content,
                "embeds":[
                    {
                        "url":embed.url,
                        "title":embed.title,
                        "color":embed.colour,
                        "description":embed.description,
                        "fields":[
                            {
                                "title":field.title,
                                "description":field.description
                            } for field in embed.fields
                        ],
                        "thumbnail":embed.thumbnail,
                        "footer":embed.footer
                    } for embed in message.embeds
                ],
                "timestamp":message.created_at
            }
        })
    f = open('activity-data.json','w')
    f.write(json.dumps(activity_data, indent=4, separators=(',',':')))
    f.close()

#TODO:     
#@bot.event
#async def on_message_edit(before, after):
#    if 'message_edit' not in list(activity_data):
#        activity_data.update({'message_edit'})
#    else:

@bot.command()
async def ping(ctx):
    can_delete = bot.user.permissions_in(ctx.channel).manage_messages
    await ctx.channel.send(str(int(round(bot.latency * 1000,0))) + " ms", delete_after=15 if can_delete else None)
    if can_delete:
        await asyncio.sleep(15)
        await ctx.message.delete()

@bot.command()
async def github(ctx):
    can_delete = bot.user.permissions_in(ctx.channel).manage_messages
    await ctx.channel.send("See me on GitHub! https://github.com/zeuschops/idea-train", delete_after=10 if can_delete else None)
    if can_delete:
        await asyncio.sleep(10)
        await ctx.message.delete()

@bot.command()
async def invite(ctx):
    can_delete = bot.user.permissions_in(ctx.channel).manage_messages
    await ctx.channel.send("Invite me to your server! https://discord.com/oauth2/authorize?client_id=799451713735622666&scope=bot&permissions=309668928", delete_after=10 if can_delete else None)
    if can_delete:
        await asyncio.sleep(10)
        await ctx.message.delete()

bot.run(config['token'], bot=True, reconnect=True)