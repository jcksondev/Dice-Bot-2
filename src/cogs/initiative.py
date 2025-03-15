import discord
from discord.ext import commands
import datetime
import setup

logger = setup.logging.getLogger("bot")


class Initiative(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.list = {}
        self.round = 1
        self.embed = discord.Embed(
            color=0x5D3FD3,
            title="Initiative List",
            description=f"Round {self.round}",
            timestamp=datetime.datetime.now(),
        )
        self.on = False

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
            await ctx.send("```Please enter a valid subcommand.```")

    @init.command()
    async def start(self, ctx):
        if not self.on:
            self.on = True
            self.embed.set_author(
                name=self.bot.user.display_name,
                url=None,
                icon_url=self.bot.user.avatar.url,
            )
            self.embed.clear_fields()
            self.embed.set_thumbnail(url=str(self.bot.user.avatar))
            await ctx.send(
                "```Please start rolling individual initiative scores.```"
            )
        else:
            await ctx.send(
                "```Please end the previous initiative before starting another.```"
            )

    @init.command()
    async def end(self, ctx):
        if self.on:
            self.embed.clear_fields()
            self.embed.add_field(
                name=f"Initiative lasted a total of {self.round} rounds!",
                value="",
                inline=False,
            )
            await ctx.send(embed=self.embed)
            self.round = 1
            self.list = {}
            self.on = False
        else:
            await ctx.send("```Initiative has already ended.```")

    @init.command()
    async def add(self, ctx, *args):
        if self.on:
            ROLL = self.bot.get_cog("Roll")
            if ROLL is not None:
                try:
                    input = ROLL.parse(args)
                    name = input.pop(0)
                    rolls = ROLL.d20(input)
                    self.list.update({name: rolls[-1]})
                    self.sort()
                    self.update()

                    if rolls[1] == 0:
                        await ctx.send(
                            f"**Rolls:** [ {', '.join(map(str, rolls[0]))} ]\n**Total:** {rolls[2]}"
                        )
                    else:
                        await ctx.send(
                            f"**Rolls:** [ {', '.join(map(str, rolls[0]))} ] {rolls[1]:=+3}\n**Total:** {rolls[2]}"
                        )
                except (ValueError, TypeError) as e:
                    await ctx.send("```Invalid arguments, please try again.```")
                    logger.exception(e)
        else:
            await ctx.send("```Please start the initiative.```")

    @init.command()
    async def insert(self, ctx, *args):
        if self.on:
            try:
                self.list.update({args[0]: int(args[1])})
                self.sort()
                self.update()
                await ctx.send(
                    f"```{args[0]} has been added to the initiative count.```"
                )
            except (ValueError, TypeError) as e:
                await ctx.send("```Invalid arguments, please try again.```")
                logger.exception(e)
        else:
            await ctx.send("```Please start the initiative.```")

    @init.command()
    async def remove(self, ctx, *args):
        if self.on:
            try:
                self.list.pop(args[0])
                self.update()
                await ctx.send(embed=self.embed)
            except KeyError as e:
                await ctx.send(
                    f"```{args[0]} is not in the initiative order.```"
                )
                logger.exception(e)
        else:
            await ctx.send("```Please start the initiative.```")

    @init.command()
    async def change(self, ctx, *args):
        if self.on:
            try:
                self.list[args[1]] = self.list.pop(args[0])
                self.update()
                await ctx.send(embed=self.embed)
            except KeyError as e:
                await ctx.send(
                    f'```"{args[0]}" is not in the initiative order.```'
                )
                logger.exception(e)
        else:
            await ctx.send("```Please start the initiative.```")

    @init.command()
    async def increment(self, ctx):
        if self.on:
            self.round = self.round + 1
            self.embed.description = f"Round {self.round}"
            await ctx.send(f"```Round: {self.round}```")
        else:
            await ctx.send("```Please start the initiative.```")

    @init.command()
    async def list(self, ctx):
        if self.on:
            await ctx.send(embed=self.embed)
        else:
            await ctx.send("```Please start the initiative.```")


async def setup(bot):
    await bot.add_cog(Initiative(bot))
