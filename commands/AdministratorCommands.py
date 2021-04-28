import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import time

class AdministratorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner():
        async def predicate(ctx):
            return ctx.author.id == 454598334448009216 #My personal ID
        return commands.check(predicate)
    
    def is_in_guild(guild_id):
        async def predicate(ctx):
            return ctx.guild.id == guild_id
        return commands.check(predicate)

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member):
        perms = ctx.message.author.permissions_in(ctx.channel)
        if perms.ban_members or perms.administrator:
            await member.guild.ban(member)
            await ctx.send("%s#%s (%s) has been banned.".format(member.name, str(member.discriminator), str(member.id)))

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member):
        user_perms = ctx.message.author.permissions_in(ctx.channel)
        if user_perms.kick_members or user_perms.administrator:
            await member.guild.kick(member)
            await ctx.send("%s#%s (%s) has been kicked.".format(member.name, str(member.discriminator), str(member.id)))
        else:
            await ctx.send("You do not have permission to use this command.", timeout=15)

    @commands.command()
    @has_permissions(manage_messages=True)
    async def clean(self, ctx, count:int):
        user_perms = ctx.message.author.permissions_in(ctx.channel)
        if user_perms.administrator or user_perms.manage_messages:
            await ctx.channel.purge(limit=count)
            await ctx.send("Deleted " + str(count) + " messages", delete_after=10)
        else:
            await ctx.send("You do not have permission to use this command.", timeout=15)

    @commands.command(hidden=True)
    @is_owner()
    @is_in_guild(609654287600975874) #In my personal guild
    async def restart(self, ctx, *, module:str):
        await self.bot.logout()
        print("Disconnected from Discord and closed all connections...")