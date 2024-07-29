import discord
from discord.ext import commands
import random
import settings

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.display_name} #{bot.user.discriminator}: (ID: {bot.user.id})')

@bot.command()
async def rr(ctx, *args):
    arguments = ''.join(args).lower().replace(',', '')
    rolls = []
    total = 0
    modifier = 0

    nat1 = '**that\'s rough buddy..**'
    nat20 = '**Natural 20!**'

    adv = 'adv' in arguments
    dis = 'dis' in arguments
    if '+' in arguments or '-' in arguments:
        modifier = int(arguments[0:2])

    if adv or dis:
        for _ in range(2):
            rolls.append(random.randint(1,20))

        if adv:
            total = max(rolls) + modifier
        else: 
            total = min(rolls) + modifier
    else:
        rolls.append(random.randint(1,20))
        total = rolls[0] + modifier

    rolls = ', '.join(map(str, rolls))
    message = f'**Rolls**: [ {rolls} ] {arguments[0]} {arguments[1]} \n**Total**: {total}'
    if total + -modifier == 20: await ctx.send(f'{message}\n{nat20}')
    elif total + -modifier == 1: await ctx.send(f'{message}\n{nat1}')
    else: await ctx.send(message)


bot.run(settings.TOKEN)