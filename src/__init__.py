import setup
import discord
from discord.ext import commands

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='.', intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user.name}')

    bot.run(setup.TOKEN)


if __name__ == "__main__":
    main()
