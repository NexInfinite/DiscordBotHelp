import discord
import asyncio
from discord.ext import commands, tasks

TOKEN = "YOUR_TOKEN"
bot = commands.Bot(command_prefix="!")

startup_extensions = []


@bot.event
async def on_ready():
    # On read, after startup
    print(f"Connecting...\nConnected {bot.user}\n")  # Send message on connected


if __name__ == "__main__":  # When script is loaded, this will run
    bot.remove_command("help")
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)  # Loads cogs successfully
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))  # Failed to load cog, with error


async def delete_loop():
    while True:
        channel = bot.get_channel(000000)  # Change this
        delete_array = []
        async for message in channel.history():
            if message.author.id != 00000:  # Change this
                delete_array.append(message)
        await channel.delete_messages(delete_array)
        await asyncio.sleep(600)


bot.run(TOKEN)  # Run bot with token
