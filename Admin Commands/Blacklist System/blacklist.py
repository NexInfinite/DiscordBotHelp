import discord
from discord.ext import commands

class Blacklist(commands.Cog,name='blacklist',command_attrs=dict(hidden=True)):
  """Blacklist people from using your bot"""
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        with open('blacklist.json') as f:
            self.blacklist = json.load(f)
            bot.add_check(self.blacklist_check)
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
    
    @blacklist.command(usage="tp!blacklist a <user>")
    @commands.check(permissions.is_owner)
    async def a(self, ctx, user: discord.User):
        """Add a user to blacklist"""
        if user.id in self.blacklist:   
            return await ctx.send("This user has already been blacklisted.")
        with open('blacklist.json', 'w') as f:
            self.blacklist.append(user.id)
            json.dump(self.blacklist, f)
        await ctx.send(f"{user} has been added to the blacklist.")
        
    @blacklist.command(usage="tp!blacklist r <user>")
    @commands.check(permissions.is_owner)
    async def r(self, ctx, user: discord.User):
        """Remove a user from blacklist."""
        if user.id in self.blacklist:
            self.blacklist.remove(user.id)
            await ctx.send(f"{user} has been removed from the blacklist.")         
        else:
            await ctx.send("You cant remove someone from blacklist if they arent blacklisted.")
        with open('blacklist.json', 'w') as f:
            json.dump(self.blacklist, f)
            

def setup(bot):
    bot.add_cog(Admin(bot))
