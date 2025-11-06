import aiohttp
import asyncio
import logging
from discord.ext import commands

class DuckPhoto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        if self.session:
            await self.session.close()

    @commands.hybrid_command(name="duck", description="summon a duck")
    async def duck(self, ctx):
        url = "https://random-d.uk/api"
        headers = {
            "Accept": "application/json",
            "User-Agent": "DiscordBot (https://github.com/youruser/DiscordBot, 1.0)"
        }
        try:
            async with self.session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    duck = data.get("duck")
                    if duck:
                        await ctx.send(duck)
                        return
                    await ctx.send("Couldn't fetch a joke right now. Try again later.")
        except asyncio.TimeoutError:
            await ctx.send("Request timed out. Try again later.")
        except Exception:
            logging.exception("Failed to fetch duck")
            await ctx.send("Error fetching duck.")

async def setup(bot):
    await bot.add_cog(DuckPhoto(bot))