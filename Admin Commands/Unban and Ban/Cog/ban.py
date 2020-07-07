import discord
from discord.ext import commands


class Ban(commands.Cog, name="Ban"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    async def ban(self, ctx, user: discord.User, *, reason=None):
        """Ban a user"""
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user.mention} has been banned")


def setup(bot):
    bot.add_cog(Ban(bot))
