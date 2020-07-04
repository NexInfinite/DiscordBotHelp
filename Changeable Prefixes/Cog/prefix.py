import discord
from discord.ext import commands

from json_commands import *


class Prefix(commands.Cog, name="Prefix"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prefix")
    async def change_prefix(self, ctx, *, new_prefix: str = None):
        """Change the prefix of the bot for your server."""
        with open("prefixes.json") as f:
            prefixes = json.load(f)

        if new_prefix is None:
            embed = discord.Embed(color=discord.Color.dark_blue())
            embed.set_author(name=f"The prefix is {prefixes[str(ctx.guild.id)]}")
            await ctx.send(embed=embed)
        else:
            prefixes[str(ctx.guild.id)] = new_prefix

            with open("prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=2)

            embed = discord.Embed(description=f"The new prefix is `{new_prefix}`",
                                  color=discord.Color.dark_blue())
            embed.set_author(name=f"Prefix changed!")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Prefix(bot))
