from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands


class WebHooks(commands.Cog, name="WebHooks"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="send")
    async def send(self, ctx, *, message):
        """Send a message as a webhook"""
        looking_webhooks = await ctx.channel.webhooks()
        if looking_webhooks:
            for webhook in looking_webhooks:
                if webhook.name == "NexInfinite-GitHub":
                    await send_webhook(webhook, message, ctx)
                    return
                else:
                    pass
        webhook = await ctx.channel.create_webhook(name="NexInfinite-GitHub")
        await send_webhook(webhook, message, ctx)
        return


def setup(bot):
    bot.add_cog(WebHooks(bot))


async def send_webhook(webhook, message, ctx):
    webhook_id = webhook.id
    webhook_token = webhook.token
    webhook = Webhook.partial(int(webhook_id),
                              f"{webhook_token}",
                              adapter=RequestsWebhookAdapter())
    webhook.send(f'{message}', username=f"{ctx.author.display_name}",
                 avatar_url=ctx.author.avatar_url)  # Sends the message as the author
    delete_array = [ctx.message]
    await ctx.channel.delete_messages(delete_array)  # Remove the command to make things look cleaner - optional
