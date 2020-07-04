import json
from types import MappingProxyType

import discord
from discord.ext import commands


# Here's a link to the original source https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b. This has been eddited


class Help(commands.Cog, name="Help"):
    """The help command!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, *, command=None):
        """Gets all category and commands of mine."""
        prefix = self.bot.command_prefix  # If you are using a bot with customizable prefixes, change the prefix here.
        try:
            if command is None:
                """Command listing.  What more?"""
                halp = discord.Embed(color=discord.Color.dark_blue())
                halp.set_author(name="All commands", icon_url=self.bot.user.avatar_url)
                mp = MappingProxyType(self.bot.cogs)
                for x in self.bot.cogs:
                    if x.lower() == "help":
                        continue
                    cog_info = mp[x]
                    all_commands = []
                    for y in cog_info.walk_commands():
                        all_commands.append(f"`{y.name}`")
                    halp.add_field(name=x, value=", ".join(all_commands), inline=False)
                halp.set_footer(text=f"To find out more about a command please do: {prefix}help <command name>")
                await ctx.send(embed=halp)
            else:
                """Command listing within a category."""
                found = False
                for x in self.bot.walk_commands():
                    if x.name.lower() == command.lower():
                        params = []
                        paramsDict = list(x.clean_params.items())
                        for i in range(len(x.clean_params)):
                            if str(paramsDict[i][1])[-5:] == "=None":
                                params.append(f"[{str(paramsDict[i][0])}]")
                            else:
                                params.append(f"<{str(paramsDict[i][0])}>")
                        aliases = []
                        for alias in x.aliases:
                            aliases.append(f"`{alias}`")
                        halp = discord.Embed(color=discord.Color.dark_blue())
                        halp.set_author(name=f"{prefix}{x.name} info", icon_url=self.bot.user.avatar_url)
                        halp.add_field(name="Description:", value=x.help, inline=False)
                        halp.add_field(name="Usage:", value=f"`{prefix}{x.name} {' '.join(params)}`", inline=False)
                        if aliases:
                            halp.add_field(name="Aliases", value=', '.join(aliases), inline=False)
                        await ctx.send(embed=halp)
                        return
                if not found:
                    """Reminds you if that category doesn't exist."""
                    halp = discord.Embed(title='Error!', description=f'Command `{command}` was not found.',
                                         color=discord.Color.red())
                    await ctx.send(embed=halp)
                else:
                    # await ctx.message.add_reaction(emoji='✔️')
                    pass
        except ValueError:
            await ctx.send("Excuse me, I can't send embeds.")


def setup(bot):
    bot.add_cog(Help(bot))
