# Welcome
These are some of the tips and tricks I have learnt. Below contains code snippets and explanations on how these work and examples of how to use them. Enjoy!

# On Message and Commands
It is always useful to have an `on_message` listener when making complicated bots. This can be used for logging commands into a channel or for a point system for each user where it tracks their messages. This can be all good until you realise that if you have `on_message` and `commands.command()` the commands wont work. A simple work around for this is:
<br>
<br>
`
await bot.process_commands(message)
`
<br>
### Example:
```python
from discord.ext import commands

bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_message(message):
    if message.author != bot.user:
        # Add the users points up
        await bot.process_commands(message)
```

