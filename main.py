import discord
import config
import os
import asyncio
from discord.ext import commands


#Bot Initialization  
class twitter_relay(commands.Bot):
    async def on_ready(self):
        await client.change_presence(status=discord.Status.do_not_disturb)
        print(f'{client.user.name} Has Awakened.')

intents = discord.Intents.all()
client = twitter_relay(command_prefix='.', intents=intents)

#Logger Initialization
logger = config.logging.getLogger('client')
discord.utils.setup_logging(root=True)

#Loading...
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with client:
        await load_cogs()
        await client.start(config.DISCORD_TOKEN)

#Runs Bot
if __name__ == '__main__':
    asyncio.run(main())
