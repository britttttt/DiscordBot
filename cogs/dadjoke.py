import aiohttp
import asyncio
import logging
from discord.ext import commands

class DadJoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        if self.session:
            await self.session.close()

    @commands.command(name="dadjoke")
    async def dadjoke(self, ctx):
        url = "https://icanhazdadjoke.com/"
        headers = {
            "Accept": "application/json",
            "User-Agent": "DiscordBot (https://github.com/youruser/DiscordBot, 1.0)"
        }
        try:
            async with self.session.get(url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    joke = data.get("joke")
                    if joke:
                        await ctx.send(joke)
                        return
                await ctx.send("Couldn't fetch a joke right now. Try again later.")
        except asyncio.TimeoutError:
            await ctx.send("Request timed out. Try again later.")
        except Exception:
            logging.exception("Failed to fetch dad joke")
            await ctx.send("Error fetching joke.")

async def setup(bot):
    await bot.add_cog(DadJoke(bot))