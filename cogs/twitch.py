import os
import time
import logging
import asyncio
import aiohttp
import discord
from discord.ext import commands


class TwitchMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self.task = None

        self.client_id = os.getenv("TWITCH_CLIENT_ID")
        self.client_secret = os.getenv("TWITCH_CLIENT_SECRET")
        self.username = os.getenv("TWITCH_USERNAME")
        self.announce_channel_id = os.getenv("TWITCH_ANNOUNCE_CHANNEL_ID")
        self.poll_interval = int(os.getenv("TWITCH_POLL_INTERVAL", "60"))

        self._token = None
        self._token_expiry = 0
        self._last_stream_id = self._load_last_stream_id()

    async def cog_load(self):
        if not all([self.client_id, self.client_secret, self.username, self.announce_channel_id]):
            logging.info("Twitch monitor disabled: missing TWITCH_* env vars")
            return
        self.session = aiohttp.ClientSession()
        self.task = asyncio.create_task(self._monitor())
        logging.info("Twitch monitor started for user: %s", self.username)

    async def cog_unload(self):
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        if self.session:
            await self.session.close()
        logging.info("Twitch monitor stopped.")

    def _load_last_stream_id(self):
        try:
            with open("last_stream_id.txt", "r", encoding="utf-8") as f:
                return f.read().strip() or None
        except FileNotFoundError:
            return None

    def _save_last_stream_id(self, stream_id):
        try:
            with open("last_stream_id.txt", "w", encoding="utf-8") as f:
                f.write(stream_id or "")
        except Exception as e:
            logging.warning("Failed to save last_stream_id: %s", e)

    async def _get_app_token(self):
        if self._token and time.time() < self._token_expiry - 30:
            return self._token

        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        async with self.session.post(url, params=params, timeout=10) as resp:
            data = await resp.json()
            if resp.status != 200 or "access_token" not in data:
                raise RuntimeError(f"Twitch auth failed: {data}")
            self._token = data["access_token"]
            self._token_expiry = time.time() + int(data.get("expires_in", 3600))
            return self._token

    async def _check_stream(self, token):
        url = "https://api.twitch.tv/helix/streams"
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {token}",
            "User-Agent": "DiscordTwitchMonitor/1.0 (bot@example.com)",
        }
        params = {"user_login": self.username}
        async with self.session.get(url, headers=headers, params=params, timeout=10) as resp:
            if resp.status == 429:
                logging.warning("Twitch API rate limited — backing off 2 minutes")
                await asyncio.sleep(120)
                return None
            elif resp.status >= 500:
                logging.warning("Twitch API server error: %s", resp.status)
                return None
            elif resp.status != 200:
                logging.warning("Twitch API error: %s", resp.status)
                return None

            data = await resp.json()
            streams = data.get("data", [])
            return streams[0] if streams else None

    async def _get_game_name(self, token, game_id: str):
        if not game_id:
            return None
        url = "https://api.twitch.tv/helix/games"
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {token}",
            "User-Agent": "DiscordTwitchMonitor/1.0 (bot@example.com)",
        }
        params = {"id": game_id}
        async with self.session.get(url, headers=headers, params=params, timeout=10) as resp:
            if resp.status != 200:
                logging.warning("Twitch API game lookup failed: %s", resp.status)
                return None
            data = await resp.json()
            games = data.get("data", [])
            return games[0].get("name") if games else None

    async def _monitor(self):
        while not self.bot.is_closed():
            try:
                token = await self._get_app_token()
                stream = await self._check_stream(token)

                if stream:
                    stream_id = stream.get("id")
                    if stream_id != self._last_stream_id:
                        # New stream detected
                        self._last_stream_id = stream_id
                        self._save_last_stream_id(stream_id)

                        title = stream.get("title", "Live on Twitch!")
                        game_id = stream.get("game_id")
                        game_name = await self._get_game_name(token, game_id)
                        thumbnail_url = stream.get("thumbnail_url", "").replace("{width}", "1280").replace("{height}", "720")
                        started_at = stream.get("started_at")
                        url = f"https://twitch.tv/{self.username}"

                        embed = discord.Embed(
                            title=title,
                            url=url,
                            description=f"Streaming **{game_name or 'Unknown Game'}**\n",
                            color=discord.Color.purple(),
                            timestamp=discord.utils.parse_time(started_at) if started_at else None,
                        )
                        embed.set_author(name=f"{self.username} is live on Twitch!", url=url)
                        embed.set_image(url=thumbnail_url)
                        embed.set_footer(text="Twitch")

                        channel = self.bot.get_channel(int(self.announce_channel_id))
                        if channel is None:
                            try:
                                channel = await self.bot.fetch_channel(int(self.announce_channel_id))
                            except Exception:
                                logging.warning("Could not fetch Twitch announce channel ID: %s", self.announce_channel_id)
                                channel = None

                        if channel:
                            await channel.send(content=" **Streaming now**", embed=embed)
                            logging.info("Announced Twitch live stream: %s (%s)", title, game_name or "Unknown game")

                else:
                    if self._last_stream_id:
                        await asyncio.sleep(30)
                        confirm = await self._check_stream(token)
                        if not confirm:
                            self._last_stream_id = None
                            self._save_last_stream_id(None)
                            logging.info("%s went offline.", self.username)

            except asyncio.CancelledError:
                break
            except Exception:
                logging.exception("Twitch monitor encountered an error.")

            await asyncio.sleep(self.poll_interval)


async def setup(bot):
    await bot.add_cog(TwitchMonitor(bot))