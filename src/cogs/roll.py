import discord
from discord.ext import commands
import random


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rolls = []
        self.total = 0
        self.modifier = 0

    def parse(self, args: tuple):
        return (
            "".join(args)
            .replace("+", " + ")
            .replace("-", " - ")
            .replace("adv", " adv ")
            .replace("dis", " dis ")
            .split()
        )

    def output(self):
        if self.modifier == 0:
            return f"**Rolls:** [ {', '.join(self.rolls)} ]\n**Total:** {self.total}"
        else:
            return f"**Rolls:** [ {', '.join(self.rolls)} ] {self.modifier:=+4}\n**Total:** {self.total}"

    def reset(self):
        self.rolls = []
        self.total = 0
        self.modifier = 0

    @commands.command()
    async def r(self, ctx, *args):
        input = self.parse(args)

        for i, arg in enumerate(input):
            if "d" in arg:
                arg = arg.split("d")
                if arg[0] == "":
                    arg[0] = 1

                for _ in range(int(arg[0])):
                    roll = random.randint(1, int(arg[1]))
                    if roll == int(arg[1]):
                        self.rolls.append(f"**{str(roll)}**")
                    else:
                        self.rolls.append(str(roll))
                    self.total = self.total + roll
            elif "+" in arg or "-" in arg:
                continue
            else:
                roll = int("".join([input[i - 1], input[i]]))
                self.modifier = roll
                self.total = self.total + roll

        await ctx.send(self.output())
        self.reset()

    @commands.command()
    async def rr(self, ctx, *args):
        input = self.parse(args)

        for i, arg in enumerate(input):
            if "adv" in arg or "dis" in arg:
                temp_rolls = []
                temp_rolls.append(random.randint(1, 20))
                temp_rolls.append(random.randint(1, 20))
                if "adv" in arg:
                    self.total = self.total + max(temp_rolls)
                elif "dis" in arg:
                    self.total = self.total + min(temp_rolls)
                for i in range(2):
                    if temp_rolls[i] == 20:
                        self.rolls.append(f"**{str(temp_rolls[i])}**")
                    else:
                        self.rolls.append(str(temp_rolls[i]))
            elif "+" in arg or "-" in arg:
                continue
            else:
                roll = int("".join([input[i - 1], input[i]]))
                self.modifier = roll
                self.total = self.total + roll

        await ctx.send(self.output())
        self.reset()


async def setup(bot):
    await bot.add_cog(Roll(bot))
