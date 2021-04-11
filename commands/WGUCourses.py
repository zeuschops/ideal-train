import discord
from discord.ext import commands
import json

class WGUCourses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def course(self, ctx, course:str):
        f = open('../helper files/CourseDump.json','r')
        d = json.loads(f.read())
        f.close()
        if course.upper() in list(d):
            await ctx.send(course + ' has course named, ' + d[course.upper()])
        else:
            await ctx.send("Unknown course.")
