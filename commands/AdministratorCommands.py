import discord
from discord.ext import commands

class AdministratorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member:discord.Member):
        await member.guild.ban(member)
        await ctx.send("%s#%s (%s) has been banned.".format(member.name, str(member.discriminator), str(member.id)))

    @commands.command()
    async def kick(self, ctx, member:discord.Member):
        user_perms = ctx.message.author.permissions_in(ctx.channel)
        if user_perms.kick_members or user_perms.administrator:
            await member.guild.kick(member)
            await ctx.send("%s#%s (%s) has been kicked.".format(member.name, str(member.discriminator), str(member.id)))
        else:
            await ctx.send("You do not have permission to use this command.", timeout=15)

    @commands.command()
    async def clear(self, ctx, count:int):
        user_perms = ctx.message.author.permissions_in(ctx.channel)
        if user_perms.administrator or user_perms.manage_messages:
            await ctx.channel.purge(limit=count)
            await ctx.send("Deleted " + str(count) + " messages", delete_after=10)
        else:
            await ctx.send("You do not have permission to use this command.", timeout=15)