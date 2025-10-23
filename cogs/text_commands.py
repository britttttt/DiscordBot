from discord.ext import commands

class TextCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        content = message.content.lower()
        if content == "69" or "sixty-nine" in content:
            await message.channel.send("nice")


async def setup(bot):
    await bot.add_cog(TextCommands(bot))
