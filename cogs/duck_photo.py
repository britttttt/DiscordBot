import aiohttp
import asyncio
import logging
import discord
from discord.ext import commands

log = logging.getLogger(__name__)

class DuckPhoto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self._timeout = aiohttp.ClientTimeout(total=10)

    async def cog_load(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=self._timeout)

    async def cog_unload(self):
        if self.session:
            try:
                await self.session.close()
            except Exception:
                log.exception("Error closing aiohttp session")

    @commands.hybrid_command(name="duck", description="Summon a random duck image")
    async def duck(self, ctx):
        """
        Fetches a random duck image from random-d.uk and posts it as an embed.
        Uses the v2 API /random endpoint which returns JSON: {"url": "...", "message": "..."}
        """

        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self._timeout)

        api_url = "https://random-d.uk/api/v2/random"
        headers = {
            "Accept": "application/json",
            "User-Agent": "DiscordBot (https://github.com/youruser/DiscordBot, 1.0)"
        }

        try:
            async with self.session.get(api_url, headers=headers) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    log.warning("Duck API returned status %s: %s", resp.status, body[:300])
                    await self._safe_send(ctx, "Couldn't fetch a duck right now. Try again later.")
                    return

                data = await resp.json(content_type=None)
                image_url = data.get("url") or data.get("image") or data.get("file")
                message = data.get("message")

                if not image_url:
                    log.warning("Duck API JSON did not contain an image URL: %s", data)
                    await self._safe_send(ctx, "Unexpected response from duck API. Try again later.")
                    return

                embed = discord.Embed(description=message or "Here's a duck 🦆")
                embed.set_image(url=image_url)
                await self._safe_send(ctx, embed=embed)
                return

        except asyncio.TimeoutError:
            log.exception("Duck request timed out")
            await self._safe_send(ctx, "Request timed out. Try again later.")
        except aiohttp.ClientError:
            log.exception("HTTP error when fetching duck")
            await self._safe_send(ctx, "Network error fetching duck. Try again later.")
        except Exception:
            log.exception("Failed to fetch duck")
            await self._safe_send(ctx, "An error occurred while fetching a duck.")

    async def _safe_send(self, ctx, content: str | None = None, *, embed: discord.Embed | None = None):
        """
        Send a response that works for both prefix and slash invocations.
        - If invoked as a slash (Interaction) and the interaction has not been responded to,
          use interaction.response.send_message.
        - Otherwise use ctx.send().
        """
        interaction = getattr(ctx, "interaction", None)
        try:
            if interaction is not None and hasattr(interaction, "response"):
                if not interaction.response.is_done():
                    await interaction.response.send_message(content=content, embed=embed)
                    return
                await interaction.followup.send(content=content, embed=embed)
                return
        except Exception:
            log.exception("Sending via Interaction failed, falling back to ctx.send")

        await ctx.send(content=content, embed=embed)

async def setup(bot):
    await bot.add_cog(DuckPhoto(bot))