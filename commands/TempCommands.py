import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class TempCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(manage_roles=True)
    async def fixpink(self, ctx):
        guild = self.bot.get_guild(600152872767979523)
        chnl = guild.get_channel(600156558692712478)
        msg = None
        async for message in chnl.history(limit=10):
            if message.id == 830583623832174592:
                msg = message
                break
        print("GUILD ID:", guild.id)
        print("CHNL ID:", chnl.id)
        print("MSG ID:", msg.id)
        user_ids = []
        for reaction in msg.reactions:
            if type(reaction.emoji) is discord.PartialEmoji:
                if reaction.emoji.id == 830583623832174592:
                    async for user in reaction.users():
                        user_ids.append(user.id)
        print("USER IDs:", user_ids)
        users = 0
        async for member in guild.fetch_members(limit=None):
            if member.id not in user_ids:
                for role in member.roles:
                    if role.id == 810005266791399434:
                        print("Removing pink role for member:", member.name, member.discriminator, member.id)
                        await member.remove_roles(role)
                        users += 1
        await ctx.send("Removed %i users's pink role." % users)