import discord
import json
import math
from discord.ext import commands


# Before reading:
# It is worth learning a little bit about how Cogs work and how discord.py works. If you have some basic knowledge; this should be useful for you.
# It is also worthy noting that my comments are a little M A D so prepare yourself for some epic and cool comments.
# OH! Its also worth nothing (yes it is worth it) that the way this works is by reading from the Pages.json file.


# The definitions below are a snippet of my json_commands.py file. You can just add:
# from json_commands import *
# And then remove the definition below

def open_json(file):
    with open(file) as f:
        data = json.load(f)
    return data


def save_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)


# The Cog Pog (Feel free to use that name - Its very spicy)

class Pages(commands.Cog, name="Pages"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Pages")
    async def pages(self, ctx):
        """Shoe me the Pages!"""
        page_limit = 3  # This variable determines the length of each page! I bet you are happy i told you that!
        current_page = 1  # This variable determines the page it starts off on!!!!!!! Honestly, you'd be lost without me. I'd recommend not changing this because you will have to edit the initial_embed.
        data = open_json("../pages.json")
        pages = math.ceil(len(data) / page_limit)
        initial_embed = discord.Embed(description=f"Page {current_page}", color=discord.Color.dark_blue())
        for x in range(page_limit):
            initial_embed.add_field(name=data[x]['name'], value=data[x]['description'], inline=False)
        msg = await ctx.send(embed=initial_embed)
        # Adding reactions
        await msg.add_reaction('\u23ee')
        await msg.add_reaction('\u25c0')
        await msg.add_reaction('\u25b6')
        await msg.add_reaction('\u23ed')
        while True:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     check=lambda r, m: m != self.bot.user and r.message.id == msg.id)  # Checking if the reaction message is the same as the sent message and the reaction user is not the bot.
            await reaction.remove(user)  # We remove the users reaction because the wait_for is waiting for a reaction add, if we dont remove it then the user has to tap twice which is kinda cringe (https://www.youtube.com/watch?v=DWtpNPZ4tb4)
            if reaction.emoji == '\u23ee':
                current_page = 1
            elif reaction.emoji == '\u25c0':
                if current_page != 1:
                    current_page -= 1
            elif reaction.emoji == '\u25b6':
                if current_page != pages:
                    current_page += 1
            elif reaction.emoji == '\u23ed':
                current_page = pages
            # Generating the next page embed
            next_page = discord.Embed(description=f"Page {current_page}", color=discord.Color.dark_blue())
            data = open_json("../pages.json")
            for x in range(page_limit * current_page - page_limit,
                           page_limit * current_page):  # That was some cool and epic maths
                try:
                    next_page.add_field(name=data[x]['name'], value=data[x]['description'], inline=False)
                except IndexError:
                    pass
            await msg.edit(embed=next_page)  # Send it then scoopidy loop loop, loopidy scoop scoop. Scoop de scoop de loop

    # If you want to be really cool (https://www.youtube.com/watch?v=39k0mmjlo0M) you can add this!
    # Syntax: !additem "This is the header" This is the description
    @commands.command(name="additem")
    async def add_item(self, ctx, name, *, description):
        """Pages 2 electric 2"""
        new_item = {
            "name": name,
            "description": description
        }
        data = open_json("../pages.json")
        data.append(new_item)
        save_json(data, "../pages.json")
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_author(name="Item has been added.")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Pages(bot))
