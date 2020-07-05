# Tips and Tricks

## Welcome

These are some of the tips and tricks I have learnt. Below contains code snippets and explanations on how these work and examples of how to use them. Enjoy!

## On Message and Commands

It is always useful to have an `on_message` listener when making complicated bots. This can be used for logging commands into a channel or for a point system for each user where it tracks their messages. This can be all good until you realise that if you have `on_message` and `commands.command()` the commands wont work. A simple work around for this is:   
   


```python
await bot.process_commands(message)
```

### Example

```python
from discord.ext import commands
import discord

bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_message(message):
    if message.author != bot.user:
        # Add the users points up
        await bot.process_commands(message)

@commands.command(name="hey")
async def hey(ctx):
    """A command that says 'hey'"""
    embed = discord.Embed(description=f"This command says hello to you!", 
                          color=discord.Color.dark_blue())
    embed.set_author(name=f"Hey!")
    await ctx.send(embed=embed) 

bot.run("YOUR TOKEN")
```

## Timers

Timers are very useful for simple rss feeds and changing playing statuses. Luckily, there are built in to discord.ext and so here is how to use them and some examples of timers \(known in disord.ext as tasks\).   


### Simple layout

```python
from discord.ext import tasks, commands
import asyncio

bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_read():
    await loop_task.start()

@tasks.loop()
async def loop_task():
    await loop()

async def loop():
    while True:
        # Do something
        await asyncio.sleep(30)

bot.run("YOUR TOKEN")
```

### Example

```python
import discord
from discord.ext import tasks, commands
import asyncio

bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_ready():
    await status_task.start()

@tasks.loop()
async def status_task():
    await status_loop()

async def status_loop():
    while True:
        guild_count = len(bot.guilds)
        activity = discord.Activity(name=f'a!help | {guild_count} servers!',
                                    type=discord.ActivityType.playing)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(30)

bot.run("YOUR TOKEN")
```

