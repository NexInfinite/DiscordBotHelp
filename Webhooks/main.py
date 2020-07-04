# import all needed imports

from discord.ext import commands

TOKEN = "YOUR TOKEN"  # Token
bot = commands.Bot(command_prefix="!")

startup_extensions = ["Cog.webhooks"]


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

bot.run(TOKEN)  # Run bot with token
