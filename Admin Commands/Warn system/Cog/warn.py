import discord
from discord.ext import commands, tasks
import json
import asyncio
from datetime import datetime
from datetime import timedelta

class warn(commands.Cog, name="warn"):
    """Warn users"""

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="warn")
    async def warn(self, ctx, user: discord.Member):
        """Warn a user"""
        with open("warns.json") as f:
            data = json.load(f)
        for x in data:
            if x['user_id'] == user.id:
                warns = x['warns'] + 1
                x['warns'] += 1
                if warns == 3:
                    mute_task.start(user, 1, ctx)
                    embed = discord.Embed(description=f"They now have {warns} warnings and have been muted for 1 hour.",
                                          color=discord.Color.dark_blue())
                    embed.set_author(name=f"{user.display_name} has been warned")
                    await ctx.send(embed=embed)
                elif warns == 5:
                    await ctx.guild.kick(user, reason="They were warned 5 times")
                    embed = discord.Embed(description=f"They now have {warns} warnings and have been kicked!",
                                          color=discord.Color.dark_blue())
                    embed.set_author(name=f"{user.display_name} has been warned")
                    await ctx.send(embed=embed)
                elif warns == 10:
                    await ctx.guild.ban(user, reason="There were warned 10 times")
                    embed = discord.Embed(description=f"They now have {warns} warnings and have been banned!",
                                          color=discord.Color.dark_blue())
                    embed.set_author(name=f"{user.display_name} has been warned")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f"They now have {warns} warnings.",
                                          color=discord.Color.dark_blue())
                    embed.set_author(name=f"{user.display_name} has been warned")
                    await ctx.send(embed=embed)
                with open("warns.json", "w") as f:
                    json.dump(data, f, indent=2)
                return
        now = datetime.now() + timedelta(days=1)
        new_user = {
            "user_id": user.id,
            "warns": 1,
            "warn_time": now.strftime("%m/%d/%Y")
        }
        data.append(new_user)
        with open("warns.json", "w") as f:
            json.dump(data, f, indent=2)
        embed = discord.Embed(description=f"They now have a warning.",
                              color=discord.Color.dark_blue())
        embed.set_author(name=f"{user.display_name} has been warned")
        await ctx.send(embed=embed)
        return

    @commands.has_permissions(administrator=True)
    @commands.command(name="pardon")
    async def pardon(self, ctx, user: discord.Member):
        """Pardon a user"""
        with open("warns.json") as f:
            data = json.load(f)
        for x in data:
            if x['user_id'] == user.id:
                x['warns'] = 0
                with open("warns.json", "w") as f:
                    json.dump(data, f, indent=2)
                embed = discord.Embed(description=f"They now have no warnings",
                                      color=discord.Color.dark_blue())
                embed.set_author(name=f"{user.display_name} has been pardoned")
                await ctx.send(embed=embed)
                return

    @commands.command(name="infractions")
    async def infractions(self, ctx, user: discord.Member = None):
        """See how many infractions you have"""
        with open("warns.json") as f:
            data = json.load(f)
        if user is not None:
            for x in data:
                if x['user_id'] == user.id:
                    warns = x['warns']
                    embed = discord.Embed(color=discord.Color.dark_blue())
                    embed.set_author(name=f"{user.display_name} has {warns} warnings")
                    await ctx.send(embed=embed)
                    return
        else:
            for x in data:
                if x['user_id'] == ctx.author.id:
                    warns = x['warns']
                    embed = discord.Embed(color=discord.Color.dark_blue())
                    embed.set_author(name=f"You have {warns} warnings")
                    await ctx.send(embed=embed)
                    return
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_author(name=f"You have no warnings")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open("warns.json") as f:
            data = json.load(f)
        for user in data:
            if user["user_id"] == message.author.id:
                if user["warns"] == 0:
                    now = datetime.now()
                    end = datetime.strptime(user["warn_time"], "%m/%d/%Y")
                    if now > end:
                        data.remove(user)
                        with open("warns.json", "w") as f:
                            json.dump(data, f, indent=2)
                        print(f"Removed {user.id} from the warn list to save data")



def setup(bot):
    bot.add_cog(warn(bot))


@tasks.loop(count=1)
async def mute_task(user, time, ctx):
    await mute_loop(user, time, ctx)


async def mute_loop(user, time, ctx):
    role = discord.utils.get(ctx.guild.roles, name="Muted")  # Name of role
    await user.add_roles(role)
    await asyncio.sleep(time*3600)
    await user.remove_roles(role)
    await user.send("You have been unmuted")
