import discord
from discord.ext import commands
import json

class Blacklist(commands.Cog,name='blacklist',command_attrs=dict(hidden=True)):
  """Blacklist people from using your bot"""
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        with open('blacklist.json') as f:
            self.blacklist = json.load(f)
            bot.add_check(self.blacklist_check)
  # this is mainly to make sure that the code is loading the json file if new data gets added
  
    def blacklist_check(self, ctx):
        return ctx.author.id not in self.blacklist
      
    @commands.group(invoke_without_command=True, usage="tp!blacklist <a:user> <r:user>")
    @commands.check(permissions.is_owner)
    async def blacklist(self, ctx):
        """ Blacklist users from using the bot. Send with no args to see who's blacklisted."""
        conv = commands.UserConverter()
        users = await asyncio.gather(*[conv.convert(ctx, str(_id)) for _id in self.blacklist])
        names = [user.name for user in users]
        await ctx.send('\t'.join(names) or 'No one has been blacklisted')

    @blacklist.command(usage="tp!blacklist a <user>", aliases=["a"])
    @commands.check(permissions.is_owner)
    async def add(self, ctx, user: discord.User):
        """Add a user to blacklist"""
        if user.id == ctx.author.id:
            await ctx.send("You can't blacklist yourself!")
        if user.id in self.blacklist:
            await ctx.send(f"{user} is already blacklisted!")
            await ctx.message.add_reaction('\u274C')
            return
        with open('blacklist.json', 'w') as f:
            self.blacklist.append(user.id)
            json.dump(self.blacklist, f)
        await ctx.send(f"{user} has been blacklisted!")
        await ctx.message.add_reaction('\u2705')

    @blacklist.command(usage="tp!blacklist r <user>", aliases=["r"])
    @commands.check(permissions.is_owner)
    async def remove(self, ctx, user: discord.User):
        """Remove a user from blacklist"""
        if user.id in self.blacklist:
            with open('blacklist.json', 'w') as f:
                self.blacklist.remove(user.id)
                json.dump(self.blacklist, f)
            await ctx.send(f"{user} has been removed from the blacklist.")
            await ctx.message.add_reaction('\u2705')
        else:
            await ctx.send(f"{user} is not blacklisted.")
            await ctx.message.add_reaction('\u274C')

    @blacklist.command(name="clear")
    @commands.check(permissions.is_owner)
    async def blacklist_clear(self, ctx):
        """ Clear the blacklist. """
        self.blacklist = []
        with open('blacklist.json', 'w') as f:
            json.dump(self.blacklist, f)
        await ctx.send("Blacklist cleared")

async def setup(bot):
    await bot.add_cog(Blacklist(bot))
