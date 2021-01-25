import requests
import discord
from discord.ext import commands

class VersionRequests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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