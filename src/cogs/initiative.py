import discord
from discord.ext import commands


class Initiative(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.list = {}
        self.pointer = 0
        self.round = 0

    def sort(self):
        self.list = {
            k: v
            for k, v in sorted(
                self.list.items(), key=lambda item: item[1], reverse=True
            )
        }

    @commands.group()
    async def init(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please enter a valid subcommand.")

    @init.command()
    async def start(self, ctx):
        await ctx.send("Initiative started.")

    @init.command()
    async def end(self, ctx):
        await ctx.send("Initiative cleared.")

    @init.command()
    async def add(self, ctx, *args):
        ROLL = self.bot.get_cog("Roll")
        if ROLL is not None:
            input = ROLL.parse(args)
            name = input.pop(0)
            rolls = ROLL.d20(input)
            self.list.update({name: rolls[-1]})
            self.sort()
            await ctx.send(self.list.items())

    @init.command()
    async def remove(self, ctx, *args):
        try:
            self.list.pop(args[0])
            await ctx.send(self.list.items())
        except KeyError:
            await ctx.send(f"{args[0]} is not in the initiative order.")

    @init.command()
    async def change(self, ctx, *args):
        try:
            self.list[args[1]] = self.list.pop(args[0])
            await ctx.send(self.list.items())
        except KeyError:
            await ctx.send(f'"{args[0]}" is not in the initiative order.')


async def setup(bot):
    await bot.add_cog(Initiative(bot))
