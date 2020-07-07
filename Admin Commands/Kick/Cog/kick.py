import discord
from discord.ext import commands

from json_commands import *


class kick(commands.Cog, name="kick"):
    """Kick a user"""

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="kick")
    async def kick(self, ctx, user: discord.User, *, reason=None):
        """Kick a user"""
        await ctx.guild.kick(user, reason)
        await ctx.send(f"{user.display_name} has been kicked!")


def setup(bot):
    bot.add_cog(kick(bot))
