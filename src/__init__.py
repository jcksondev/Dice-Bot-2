import setup
import discord
from discord.ext import commands

def main():
    logger = setup.logging.getLogger('bot')

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='.', intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"Logged in as {bot.user.name} #{bot.user.discriminator}")

        for cog in setup.COGS_DIR.glob("*.py"):
            if cog.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog.name[:-3]}")

    bot.run(setup.TOKEN, root_logger=True)


if __name__ == "__main__":
    main()
