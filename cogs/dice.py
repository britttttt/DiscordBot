import random
from discord.ext import commands

class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="d20")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def d20(self, ctx):
        number = random.randint(1, 20)
        await ctx.send("...")
        await ctx.send("...")
        if number == 1:
            await ctx.send(f"{ctx.author.mention} uh oh diva, that is a crit fail, you rolled a {number}!💀💀💀")
        elif number == 20:
            await ctx.send(f"{ctx.author.mention} Huzzah, that is a crit success! You rolled a {number}!🎊🎊🎊")
        else:
            await ctx.send(f"{ctx.author.mention} you rolled a {number}!")

async def setup(bot):
    await bot.add_cog(Dice(bot))