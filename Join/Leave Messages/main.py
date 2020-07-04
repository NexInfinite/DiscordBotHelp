import discord
from discord.ext import commands


TOKEN = ""  # Token
bot = commands.Bot(command_prefix="!")

# Load Cogs


@bot.event
async def on_ready():
    # On read, after startup
    print(f"Connecting...\nConnected {bot.user}\n")  # Send message on connected


@bot.event
async def on_member_join(member):
    await member.guild.system_channel.send(f'Welcome, {member.name}!') # Gets the announcements channel and... welcomes the player...

@bot.event
async def on_member_remove(member):
    await member.guild.system_channel.send(f'{member.name} left :(!') # Gets the announcements channel and... shuns the player for leaving your wonderful discord server...

bot.run(TOKEN)  # Run bot with token