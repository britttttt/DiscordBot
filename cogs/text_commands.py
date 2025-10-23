# cogs/text_commands.py
import discord
from discord.ext import commands

class TextCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        msg = message.content.lower()

        if "69" in msg or "sixty nine" in msg:
            await message.channel.send("nice")

def setup(bot):
    bot.add_cog(TextCommands(bot))
