import discord
from discord.ext import commands
import random
import setup

logger = setup.logging.getLogger("bot")


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rolls = []
        self.total = 0
        self.modifier = 0
        self.on = False

    def parse(self, args: tuple):
        return (
            "".join(args)
            .replace("+", " + ")
            .replace("-", " - ")
            .replace("adv", " adv ")
            .replace("dis", " dis ")
            .split()
        )

    def output(self, natural20=False, natural1=False):
        output = ""
        if self.modifier == 0:
            output = f"**Rolls:** [ {', '.join(self.rolls)} ]\n**Total:** {self.total}"
        else:
            output = f"**Rolls:** [ {', '.join(self.rolls)} ] {self.modifier:=+3}\n**Total:** {self.total}"
        if natural20:
            output = output + "\n**Natural 20!**"
        elif natural1:
            output = output + "\n**You're Fucked**"

        return output

    def reset(self):
        self.rolls = []
        self.total = 0
        self.modifier = 0

    @commands.command()
    async def r(self, ctx, *args):
        try:
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
        except ValueError as e:
            self.reset()
            await ctx.send("```Invalid arguments, please try again.```")
            logger.exception(e)

    def d20(self, input):
        try:
            dice = [random.randint(1, 20)]
            total = dice[0]
            modifier = 0

            for i, arg in enumerate(input):
                if "adv" in arg:
                    dice.append(random.randint(1, 20))
                    total = max(dice) + modifier
                elif "dis" in arg:
                    dice.append(random.randint(1, 20))
                    total = min(dice) + modifier
                elif "+" in arg or "-" in arg:
                    continue
                else:
                    modifier = int("".join([input[i - 1], input[i]]))
                    total = total + modifier

            return [dice, modifier, total]
        except ValueError as e:
            self.reset()
            logger.exception(e)
            return ValueError

    @commands.command()
    async def rr(self, ctx, *args):
        try:
            rolls = self.d20(self.parse(args))
            natural20 = False
            natural1 = False

            for i, arg in enumerate(rolls):
                if i == 0:
                    for _, roll in enumerate(arg):
                        if roll == 20:
                            self.rolls.append(f"**{str(roll)}**")
                            natural20 = True
                        elif roll == 1:
                            self.rolls.append(str(roll))
                            natural1 = True
                        else:
                            self.rolls.append(str(roll))
                elif i == 1:
                    self.modifier = arg
                elif i == 2:
                    self.total = arg

            await ctx.send(self.output(natural20, natural1))
            self.reset()
        except (ValueError, TypeError) as e:
            self.reset()
            await ctx.send("```Invalid arguments, please try again.```")
            logger.exception(e)


async def setup(bot):
    await bot.add_cog(Roll(bot))
