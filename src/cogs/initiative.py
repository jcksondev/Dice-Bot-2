import discord
from discord.ext import commands
import datetime


class Initiative(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.list = {}
        self.round = 1
        self.embed = discord.Embed(
            color=0x5D3FD3,
            title="Initiative List",
            description="Refer to the help command for instructions.",
            timestamp=datetime.datetime.now(),
        )

    def sort(self):
        self.list = {
            k: v
            for k, v in sorted(
                self.list.items(), key=lambda item: item[1], reverse=True
            )
        }

    def update(self):
        self.embed.clear_fields()
        for k, v in self.list.items():
            self.embed.add_field(name=k, value=v, inline=False)

    @commands.group()
    async def init(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please enter a valid subcommand.")

    @init.command()
    async def start(self, ctx):
        self.embed.clear_fields()
        self.embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=self.embed)

    @init.command()
    async def end(self, ctx):
        self.embed.clear_fields()
        self.embed.add_field(
            name=f"Initiative lasted a total of {self.round} rounds!",
            value="",
            inline=False,
        )
        await ctx.send(embed=self.embed)
        self.round = 1
        self.list = {}

    @init.command()
    async def add(self, ctx, *args):
        ROLL = self.bot.get_cog("Roll")
        if ROLL is not None:
            input = ROLL.parse(args)
            name = input.pop(0)
            rolls = ROLL.d20(input)
            self.list.update({name: rolls[-1]})
            self.sort()
            self.update()
            await ctx.send(embed=self.embed)

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

    @init.command()
    async def increment(self, ctx):
        self.round = self.round + 1

    @init.command()
    async def list(self, ctx):
        await ctx.send(embed=self.embed)


async def setup(bot):
    await bot.add_cog(Initiative(bot))
