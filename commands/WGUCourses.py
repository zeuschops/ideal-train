import discord
from discord.ext import commands
import requests

class WGUCourses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def course(self, ctx, course:str):
        resp = requests.get('http://localhost:20090/wgu/courses/' + course)
        if resp.status_code != 200:
            await ctx.send('Unknown error occurred. Status code: ' + str(resp.status_code))
        else:
            await ctx.send(course + ' has course named, ' + resp.json()['course_name'])