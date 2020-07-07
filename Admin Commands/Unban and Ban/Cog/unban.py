import discord
from discord.ext import commands


class Unban(commands.Cog, name="Unban"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unban")
    async def unban(self, ctx, member, *, reason=None):
        """Unban a user"""
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name.lower() == member.lower():
                await ctx.guild.unban(user, reason=reason)
                await ctx.send(f'{user.name} was unbanned')
                return


def setup(bot):
    bot.add_cog(Unban(bot))
