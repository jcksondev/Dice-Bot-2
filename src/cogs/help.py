from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(
            """```Note: Anything wrapped in '[]' is mandatory. Anything wrapped in '{}' is optional.
            
        Roll:
            .r [Dice] {Modifier}                        # Rolls given dice string. e.g. '.r d4 + 6', '.r 4d6 + 2d8 +10'
            .rr {Modifier} {Adv/Dis}                    # Rolls a d20. e.g. '.rr +5 adv', '.rr - 1 dis'

        Initiative:
            .init start                                 # Begins initiative count.
            .init end                                   # Ends initiative count and displays number of rounds played. 
            .init add [Name] {Modifier} {Adv/Dis}       # Rolls initiative and adds character to initiative count. 
                                                            e.g. '.init add Yves +5', '.init add Vinco +11 adv'
            .init remove [Name]                         # Removes character from initiative count. Name must match exactly.
            .init insert [Name] [Value]                 # Adds character to initiative count with a predetermined value.
            .init change [Name] [New Name]              # Changes the name of a character on the initiative count while keeping the score.
            .init increment                             # Increases the round counter by 1.
            .init list                                  # Prints out the current initiative count and round count.
            ```"""
        )


async def setup(bot):
    await bot.add_cog(Help(bot))
