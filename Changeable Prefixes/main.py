import json

from discord.ext import commands


default_prefix = "!"


def get_prefix(client, message):
    with open("prefixes.json") as f:
        prefixes = json.load(f)

    try:
        prefix = prefixes[str(message.guild.id)]
    except KeyError:
        prefix = default_prefix

    return prefix


TOKEN = "YOUR TOKEN"
bot = commands.Bot(command_prefix=get_prefix)

startup_extensions = ["Cog.prefix"]


@bot.event
async def on_guild_join(guild):
    with open("prefixes.json") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = default_prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=2)


@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=2)


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
