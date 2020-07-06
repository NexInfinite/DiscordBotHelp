import discord
from discord.ext import commands


class Unban(commands.Cog, name="Unban"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unban")
    async def unban(self, ctx, user: discord.User, reason=None):
        """Unban a user"""
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"{user.mention} has been unbanned!")


def setup(bot):
    bot.add_cog(Unban(bot))
