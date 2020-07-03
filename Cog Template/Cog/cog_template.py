import discord
from discord.ext import commands


class CogTemplate(commands.Cog, name="The name that appears on the help command"):
    def __init__(self, bot):
        self.bot = bot

    # Your commands go here


def setup(bot):
    bot.add_cog(CogTemplate(bot))
