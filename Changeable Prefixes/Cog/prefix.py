import discord
from discord.ext import commands

from json_commands import *

import json


class Prefix(commands.Cog,name='prefix'):
    """Change your bots prefix for servers"""
    def __init__(self, bot):
        self.bot = bot
        with open('prefixes.json') as f:
            self.prefixes = json.load(f)
        self.bot.command_prefix = self.get_prefix
        self.default_prefix = '!'
        
    def get_prefix(self, bot, message):
        prefix = self.prefixes.get(str(message.guild.id), self.default_prefix) if getattr(message, 'guild', None) else self.default_prefix
        return commands.when_mentioned_or(prefix)(bot, message)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setprefix(self, ctx, *, new=None):
        no_prefix = discord.Embed(title="Please put a prefix you want.", colour=ColorYouWant)
        if not new:
            return await ctx.send(embed=no_prefix)
        self.prefixes[str(ctx.guild.id)] = new
        with open('prefixes.json', 'w') as f:
            json.dump(self.prefixes, f, indent=4)
        new_prefix = discord.Embed(description=f"The new prefix is `{new}`", color=ColorYouWant, timestamp=ctx.message.created_at)
        await ctx.send(embed=new_prefix)
        await ctx.guild.me.edit(nick=f'[{new}] AGB')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx):
        with open("prefixes.json") as f:
            prefixes = json.load(f)
        embed = discord.Embed(colour=ColorYouWant, timestamp=ctx.message.created_at)
        embed.add_field(name="Prefix for this server:", value=f"{prefixes[str(ctx.guild.id)]}")
        embed.set_footer(text=f"Command passed by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Prefix(bot))
